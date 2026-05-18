from typing import Any

from pysat.formula import CNF
from pysat.card import CardEnc, EncType
from pysat.pb import PBEnc

from .present import P, DDT

# A clause template is a list of (bit_index, is_positive_literal) pairs.
ClauseTemplate = list[tuple[int, bool]]


def _compute_pi_clauses(valid: set[int], invalid: set[int], nbits: int) -> list[ClauseTemplate]:
    """Quine-McCluskey minimization on an nbits-wide boolean space.

    Returns a list of clause templates. Each template is a list of
    (bit_index, is_positive) pairs encoding one prime implicant that
    covers only invalid minterms.
    """
    mask_all = (1 << nbits) - 1

    # Each implicant is (value, dont_care_mask)
    current: set[tuple[int, int]] = set()
    for v in invalid:
        current.add((v, 0))
    prime_implicants: set[tuple[int, int]] = set()

    while current:
        merged: set[tuple[int, int]] = set()
        used: set[tuple[int, int]] = set()
        imps = list(current)
        for i in range(len(imps)):
            for j in range(i + 1, len(imps)):
                v1, m1 = imps[i]
                v2, m2 = imps[j]
                if m1 != m2:
                    continue
                diff = (v1 ^ v2) & ~m1 & mask_all
                # diff must be exactly one bit
                if diff == 0 or (diff & (diff - 1)) != 0:
                    continue
                new_mask = (m1 | diff) & mask_all
                new_val = v1 & ~diff & mask_all
                # Make sure the merged implicant doesn't cover any valid minterm
                covers_valid = False
                for p in valid:
                    if (p & ~new_mask) == (new_val & ~new_mask):
                        covers_valid = True
                        break
                if not covers_valid:
                    merged.add((new_val, new_mask))
                    used.add(imps[i])
                    used.add(imps[j])
        for pi in current:
            if pi not in used:
                prime_implicants.add(pi)
        current = merged

    # For each prime implicant, find the invalid minterms it covers
    pi_coverage: list[tuple[tuple[int, int], set[int]]] = []
    for val, mask in prime_implicants:
        covered: set[int] = set()
        for p in invalid:
            if (p & ~mask) == (val & ~mask):
                covered.add(p)
        pi_coverage.append(((val, mask), covered))

    # Greedy set cover: pick the implicant covering the most uncovered minterms
    uncovered = set(invalid)
    selected: list[tuple[int, int]] = []
    while uncovered:
        pi_coverage.sort(key=lambda x: len(x[1] & uncovered), reverse=True)
        best_pi, best_covered = pi_coverage[0]
        selected.append(best_pi)
        uncovered -= best_covered
        pi_coverage = [(pi, cov) for pi, cov in pi_coverage if cov & uncovered]

    # Build clause templates from selected implicants
    clauses: list[ClauseTemplate] = []
    for val, mask in selected:
        clause: ClauseTemplate = []
        for i in range(nbits):
            if not (mask >> i) & 1:  # bit i is not a don't-care
                is_positive = not ((val >> i) & 1)
                clause.append((i, is_positive))
        clauses.append(clause)
    return clauses


def _compute_sbox_pi_clauses(ddt: Any) -> list[ClauseTemplate]:
    """8-bit compact CNF covering all invalid (input, output) DDT pairs."""
    valid: set[int] = set()
    invalid: set[int] = set()
    for a in range(16):
        for b in range(16):
            code = a | (b << 4)
            if ddt[a][b] > 0:
                valid.add(code)
            else:
                invalid.add(code)
    return _compute_pi_clauses(valid, invalid, 8)


def _compute_sbox_weight_pi_clauses(ddt: Any) -> list[ClauseTemplate]:
    """10-bit compact CNF for combined S-box validity + weight.

    Bit layout: bits 0-3 = x (input diff), 4-7 = y (output diff), 8 = active, 9 = heavy.
    Valid minterms:
      - x=0, y=0, active=0, heavy=0  (inactive S-box)
      - x=a, y=b, active=1, heavy=0  when DDT[a][b] = 4  (weight 2)
      - x=a, y=b, active=1, heavy=1  when DDT[a][b] = 2  (weight 3)
    Weight per S-box = 2*active + heavy.
    """
    valid: set[int] = {0}  # inactive S-box: all bits zero
    for a in range(1, 16):
        for b in range(16):
            if ddt[a][b] == 4:
                valid.add(a | (b << 4) | (1 << 8))           # weight 2
            elif ddt[a][b] == 2:
                valid.add(a | (b << 4) | (1 << 8) | (1 << 9))  # weight 3
    invalid: set[int] = set()
    for v in range(1 << 10):
        if v not in valid:
            invalid.add(v)
    return _compute_pi_clauses(valid, invalid, 10)


# Precompute clause templates once at import time
_SBOX_PI_TEMPLATES: list[ClauseTemplate] = _compute_sbox_pi_clauses(DDT)
_SBOX_WEIGHT_TEMPLATES: list[ClauseTemplate] = _compute_sbox_weight_pi_clauses(DDT)


def diff_var(r: int, i: int) -> int:
    """SAT variable for bit i of the difference word at round r."""
    return 1 + r * 64 + i


def active_var(R: int, r: int, s: int) -> int:
    """SAT variable: S-box s at round r is active (non-zero input difference)."""
    return 1 + 64 * (R + 1) + r * 16 + s


def heavy_var(R: int, r: int, s: int) -> int:
    """SAT variable: S-box s at round r has a weight-3 transition (DDT value = 2)."""
    return 1 + 64 * (R + 1) + R * 16 + r * 16 + s


def sbox_clauses_compact(x_vars: list[int], y_vars: list[int]) -> list[list[int]]:
    """Clauses ruling out all DDT-invalid (input, output) pairs for one S-box."""
    all_vars = x_vars + y_vars
    clauses: list[list[int]] = []
    for template in _SBOX_PI_TEMPLATES:
        clause: list[int] = []
        for bit_index, is_positive in template:
            var = all_vars[bit_index]
            clause.append(var if is_positive else -var)
        clauses.append(clause)
    return clauses


def sbox_weight_clauses_compact(x_vars: list[int], y_vars: list[int],
                                act_var: int, hvy_var: int) -> list[list[int]]:
    """Clauses encoding DDT validity and weight variables for one S-box.

    act_var = 1 iff the S-box is active (input diff != 0).
    hvy_var = 1 iff the transition has weight 3 (DDT value = 2).
    Weight contribution = 2*act_var + hvy_var.
    """
    all_vars = x_vars + y_vars + [act_var, hvy_var]
    clauses: list[list[int]] = []
    for template in _SBOX_WEIGHT_TEMPLATES:
        clause: list[int] = []
        for bit_index, is_positive in template:
            var = all_vars[bit_index]
            clause.append(var if is_positive else -var)
        clauses.append(clause)
    return clauses


def _active_clauses(cnf: CNF, R: int, r: int, s: int) -> None:
    """Add clauses linking active_var(r, s) to (input diff != 0) for S-box s."""
    a = active_var(R, r, s)
    x_bits = [diff_var(r, 4 * s + j) for j in range(4)]
    # active -> at least one input bit is 1
    cnf.append([-a] + x_bits)
    # each input bit being 1 -> active
    for xi in x_bits:
        cnf.append([-xi, a])


def build_model(R: int, active_bounds: dict[int, int] | None = None) -> CNF:
    """Build a SAT model for R-round PRESENT differential trails (active S-box count)."""
    cnf = CNF()
    for r in range(R):
        for s in range(16):
            x_vars = [diff_var(r, 4 * s + j) for j in range(4)]
            y_vars = [diff_var(r + 1, P[4 * s + j]) for j in range(4)]
            for clause in sbox_clauses_compact(x_vars, y_vars):
                cnf.append(clause)
            _active_clauses(cnf, R, r, s)
    # Input difference must be non-zero
    cnf.append([diff_var(0, i) for i in range(64)])
    if active_bounds:
        # Find the tightest known active-sbox lower bound for a prefix of rounds
        best_k = 0
        best_bound = 0
        for k, bound in active_bounds.items():
            if k < R and k > best_k:
                best_k = k
                best_bound = bound
        if best_k > 0:
            lits: list[int] = []
            for r in range(best_k):
                for s in range(16):
                    lits.append(active_var(R, r, s))
            cnf.extend(CardEnc.atleast(lits=lits, bound=best_bound,
                                       encoding=EncType.seqcounter, top_id=cnf.nv).clauses)
    return cnf


def _weight_lits_weights(R: int, r_start: int, r_end: int) -> tuple[list[int], list[int]]:
    """Return (lits, weights) lists for PBEnc over S-boxes in rounds r_start..r_end-1.

    Weight per S-box = 2*active + heavy, so each S-box contributes two literals
    with weights [2, 1].
    """
    lits: list[int] = []
    weights: list[int] = []
    for r in range(r_start, r_end):
        for s in range(16):
            lits.append(active_var(R, r, s))
            lits.append(heavy_var(R, r, s))
            weights.append(2)
            weights.append(1)
    return lits, weights


def build_weighted_model(R: int, W: int | None = None,
                         active_bounds: dict[int, int] | None = None,
                         weight_bounds: dict[int, int] | None = None) -> CNF:
    """Build a weighted SAT model for R-round PRESENT differential trails.

    Uses 10-bit prime implicant encoding: each clause encodes both DDT validity
    and the weight variable semantics. Weight = 2*active + heavy per S-box.
    """
    cnf = CNF()
    for r in range(R):
        for s in range(16):
            x_vars = [diff_var(r, 4 * s + j) for j in range(4)]
            y_vars = [diff_var(r + 1, P[4 * s + j]) for j in range(4)]
            act = active_var(R, r, s)
            hvy = heavy_var(R, r, s)
            for clause in sbox_weight_clauses_compact(x_vars, y_vars, act, hvy):
                cnf.append(clause)
    # Input difference must be non-zero
    cnf.append([diff_var(0, i) for i in range(64)])

    if weight_bounds:
        # PC1: the first `split` rounds must have total weight >= B[split]
        for split in range(1, min(R, 5)):
            b = weight_bounds.get(split, 0)
            if b > 0:
                lits, ws = _weight_lits_weights(R, 0, split)
                cnf.extend(PBEnc.atleast(lits=lits, weights=ws, bound=b,
                                         top_id=cnf.nv).clauses)
        # PC2: the last `suf_len` rounds must have total weight >= B[suf_len]
        for suf_len in range(1, min(R, 5)):
            b = weight_bounds.get(suf_len, 0)
            if b > 0:
                lits, ws = _weight_lits_weights(R, R - suf_len, R)
                cnf.extend(PBEnc.atleast(lits=lits, weights=ws, bound=b,
                                         top_id=cnf.nv).clauses)

    if active_bounds:
        best_k = 0
        best_bound = 0
        for k, bound in active_bounds.items():
            if k < R and k > best_k:
                best_k = k
                best_bound = bound
        if best_k > 0:
            lits = []
            for r in range(best_k):
                for s in range(16):
                    lits.append(active_var(R, r, s))
            cnf.extend(CardEnc.atleast(lits=lits, bound=best_bound,
                                       encoding=EncType.seqcounter, top_id=cnf.nv).clauses)

    if W is not None:
        lits, ws = _weight_lits_weights(R, 0, R)
        cnf.extend(PBEnc.atmost(lits=lits, weights=ws, bound=W, top_id=cnf.nv).clauses)

    return cnf
