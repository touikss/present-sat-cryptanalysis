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

    Args:
        valid: set of valid minterms (must not be covered by any clause).
        invalid: set of invalid minterms to cover.
        nbits: number of bits in the boolean space.
    """
    mask_all = (1 << nbits) - 1

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
                if diff == 0 or (diff & (diff - 1)) != 0:
                    continue
                new_mask = (m1 | diff) & mask_all
                new_val = v1 & ~diff & mask_all
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

    pi_coverage: list[tuple[tuple[int, int], set[int]]] = []
    for val, mask in prime_implicants:
        covered: set[int] = set()
        for p in invalid:
            if (p & ~mask) == (val & ~mask):
                covered.add(p)
        pi_coverage.append(((val, mask), covered))

    uncovered = set(invalid)
    selected: list[tuple[int, int]] = []
    while uncovered:
        pi_coverage.sort(key=lambda x: len(x[1] & uncovered), reverse=True)
        best_pi, best_covered = pi_coverage[0]
        selected.append(best_pi)
        uncovered -= best_covered
        pi_coverage = [(pi, cov) for pi, cov in pi_coverage if cov & uncovered]

    clauses: list[ClauseTemplate] = []
    for val, mask in selected:
        clause: ClauseTemplate = []
        for i in range(nbits):
            if not (mask >> i) & 1:
                is_positive = not ((val >> i) & 1)
                clause.append((i, is_positive))
        clauses.append(clause)
    return clauses


def _compute_sbox_pi_clauses(ddt: Any) -> list[ClauseTemplate]:
    """8-bit compact CNF covering all invalid (input, output) DDT pairs.

    Args:
        ddt: the S-box Difference Distribution Table (16x16 array).
    """
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

    Args:
        ddt: the S-box Difference Distribution Table (16x16 array).
    """
    valid: set[int] = {0}
    for a in range(1, 16):
        for b in range(16):
            if ddt[a][b] == 4:
                valid.add(a | (b << 4) | (1 << 8))
            elif ddt[a][b] == 2:
                valid.add(a | (b << 4) | (1 << 8) | (1 << 9))
    invalid: set[int] = set()
    for v in range(1 << 10):
        if v not in valid:
            invalid.add(v)
    return _compute_pi_clauses(valid, invalid, 10)


# Precompute clause templates once at import time
_SBOX_PI_TEMPLATES: list[ClauseTemplate] = _compute_sbox_pi_clauses(DDT)
_SBOX_WEIGHT_TEMPLATES: list[ClauseTemplate] = _compute_sbox_weight_pi_clauses(DDT)


def diff_var(r: int, i: int) -> int:
    """SAT variable for bit i of the difference word at round r.

    Args:
        r: round index.
        i: bit index (0-63).
    """
    return 1 + r * 64 + i


def active_var(R: int, r: int, s: int) -> int:
    """SAT variable: S-box s at round r is active (non-zero input difference).

    Args:
        R: total number of rounds (used for variable numbering).
        r: round index.
        s: S-box index (0-15).
    """
    return 1 + 64 * (R + 1) + r * 16 + s


def heavy_var(R: int, r: int, s: int) -> int:
    """SAT variable: S-box s at round r has a weight-3 transition (DDT value = 2).

    Args:
        R: total number of rounds (used for variable numbering).
        r: round index.
        s: S-box index (0-15).
    """
    return 1 + 64 * (R + 1) + R * 16 + r * 16 + s


def sbox_clauses_compact(x_vars: list[int], y_vars: list[int]) -> list[list[int]]:
    """Clauses ruling out all DDT-invalid (input, output) pairs for one S-box.

    Args:
        x_vars: list of 4 SAT variables for the input nibble bits.
        y_vars: list of 4 SAT variables for the output nibble bits.
    """
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

    Args:
        x_vars: list of 4 SAT variables for the input nibble bits.
        y_vars: list of 4 SAT variables for the output nibble bits.
        act_var: SAT variable for whether this S-box is active.
        hvy_var: SAT variable for whether this S-box has a weight-3 transition.
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
    """Add clauses linking active_var(r, s) to (input diff != 0) for S-box s.

    Args:
        cnf: the CNF formula to extend.
        R: total number of rounds (used for variable numbering).
        r: round index.
        s: S-box index (0-15).
    """
    a = active_var(R, r, s)
    x_bits = [diff_var(r, 4 * s + j) for j in range(4)]
    cnf.append([-a] + x_bits)
    for xi in x_bits:
        cnf.append([-xi, a])


def build_model(R: int, active_bounds: dict[int, int] | None = None) -> CNF:
    """Build a SAT model for R-round PRESENT differential trails (active S-box count).

    Args:
        R: number of rounds.
        active_bounds: optional dict mapping round count k to min active S-boxes,
                       used to add a prefix lower-bound constraint.
    """
    cnf = CNF()
    for r in range(R):
        for s in range(16):
            x_vars = [diff_var(r, 4 * s + j) for j in range(4)]
            y_vars = [diff_var(r + 1, P[4 * s + j]) for j in range(4)]
            for clause in sbox_clauses_compact(x_vars, y_vars):
                cnf.append(clause)
            _active_clauses(cnf, R, r, s)
    cnf.append([diff_var(0, i) for i in range(64)])
    if active_bounds:
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

    Args:
        R: total number of rounds (used for variable numbering).
        r_start: first round index (inclusive).
        r_end: last round index (exclusive).
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

    Args:
        R: number of rounds.
        W: optional upper bound on total trail weight (added as a hard constraint).
        active_bounds: optional dict mapping round count k to min active S-boxes.
        weight_bounds: optional dict mapping round count k to min trail weight,
                       used to add PC1/PC2 prefix and suffix lower-bound constraints.
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
    cnf.append([diff_var(0, i) for i in range(64)])

    if weight_bounds:
        for split in range(1, min(R, 5)):
            b = weight_bounds.get(split, 0)
            if b > 0:
                lits, ws = _weight_lits_weights(R, 0, split)
                cnf.extend(PBEnc.atleast(lits=lits, weights=ws, bound=b,
                                         top_id=cnf.nv).clauses)
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


def decode_trail(model: list[int], R: int) -> list[int]:
    """Decode R+1 difference words from a SAT model.

    Returns a list of R+1 64-bit integers: deltas[r] is the difference word
    at position r (deltas[0] = input diff, deltas[R] = output diff).

    Args:
        model: list of signed integers from the solver (positive = True).
        R: number of rounds.
    """
    pos = set(model)
    diffs = []
    for r in range(R + 1):
        val = 0
        for i in range(64):
            if diff_var(r, i) in pos:
                val |= (1 << i)
        diffs.append(val)
    return diffs
