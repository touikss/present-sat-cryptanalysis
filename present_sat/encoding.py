from pysat.formula import CNF
from pysat.pb import PBEnc
from math import log2

from .present import P, DDT


def _compute_pi_clauses(valid, invalid, nbits):
    """Quine-McCluskey minimization over an nbits-wide boolean space.

    Returns a greedy-minimal covering set of clause templates (prime implicants)
    that cover all invalid minterms without covering any valid ones.

    Args:
        valid: set of valid minterms (must not be covered).
        invalid: set of invalid minterms to cover.
        nbits: number of bits in the space.
    """
    mask_all = (1 << nbits) - 1

    current = set()
    for v in invalid:
        current.add((v, 0))
    prime_implicants = set()

    while current:
        merged = set()
        used = set()
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

    pi_coverage = []
    for val, mask in prime_implicants:
        covered = set()
        for p in invalid:
            if (p & ~mask) == (val & ~mask):
                covered.add(p)
        pi_coverage.append(((val, mask), covered))

    uncovered = set(invalid)
    selected = []
    while uncovered:
        pi_coverage.sort(key=lambda x: len(x[1] & uncovered), reverse=True)
        best_pi, best_covered = pi_coverage[0]
        selected.append(best_pi)
        uncovered -= best_covered
        pi_coverage = [(pi, cov) for pi, cov in pi_coverage if cov & uncovered]

    clauses = []
    for val, mask in selected:
        clause = []
        for i in range(nbits):
            if not (mask >> i) & 1:
                is_positive = not ((val >> i) & 1)
                clause.append((i, is_positive))
        clauses.append(clause)
    return clauses


def _compute_sbox_pi_clauses(ddt):
    """Build 8-bit CNF clause templates ruling out all DDT-invalid (input, output) pairs.

    Args:
        ddt: the S-box Difference Distribution Table (16x16 array).
    """
    valid = set()
    invalid = set()
    for a in range(16):
        for b in range(16):
            code = a | (b << 4)
            if ddt[a][b] > 0:
                valid.add(code)
            else:
                invalid.add(code)
    return _compute_pi_clauses(valid, invalid, 8)


def _compute_sbox_weight_pi_clauses(ddt):
    """Build 10-bit CNF clause templates encoding DDT validity and weight for one S-box.

    Bit layout: 0-3 = input diff, 4-7 = output diff, 8 = active, 9 = heavy.
    Weight per S-box = 2*active + heavy (heavy means DDT entry = 2).

    Args:
        ddt: the S-box Difference Distribution Table (16x16 array).
    """
    valid = {0}
    for a in range(1, 16):
        for b in range(16):
            if ddt[a][b] == 4:
                valid.add(a | (b << 4) | (1 << 8))
            elif ddt[a][b] == 2:
                valid.add(a | (b << 4) | (1 << 8) | (1 << 9))
    invalid = set()
    for v in range(1 << 10):
        if v not in valid:
            invalid.add(v)
    return _compute_pi_clauses(valid, invalid, 10)


_SBOX_PI_TEMPLATES = _compute_sbox_pi_clauses(DDT)
_SBOX_WEIGHT_TEMPLATES = _compute_sbox_weight_pi_clauses(DDT)


def diff_var(r, i):
    """SAT variable index for bit i of the difference word entering round r.

    Args:
        r: round index (0 = plaintext difference, R = ciphertext difference).
        i: bit index (0-63).
    """
    return 1 + r * 64 + i


def active_var(R, r, s):
    """SAT variable index for the active flag of S-box s at round r.

    Active means the S-box input difference is non-zero.

    Args:
        R: total number of rounds (used to offset variable numbering).
        r: round index.
        s: S-box index (0-15).
    """
    return 1 + 64 * (R + 1) + r * 16 + s


def heavy_var(R, r, s):
    """SAT variable index for the heavy flag of S-box s at round r.

    Heavy means the transition has DDT value 2, contributing weight 3 instead of 2.

    Args:
        R: total number of rounds (used to offset variable numbering).
        r: round index.
        s: S-box index (0-15).
    """
    return 1 + 64 * (R + 1) + R * 16 + r * 16 + s


def _apply_templates(templates, all_vars):
    """Instantiate a list of prime-implicant clause templates against concrete SAT variables.

    Args:
        templates: list of clause templates, each a list of (bit_index, is_positive) pairs.
        all_vars: list of SAT variable indices indexed by bit position.
    """
    return [
        [all_vars[i] if pos else -all_vars[i] for i, pos in template]
        for template in templates
    ]


def sbox_clauses_compact(x_vars, y_vars):
    """CNF clauses ruling out all DDT-invalid (input, output) pairs for one S-box.

    Args:
        x_vars: list of 4 SAT variable indices for the input nibble bits.
        y_vars: list of 4 SAT variable indices for the output nibble bits.
    """
    return _apply_templates(_SBOX_PI_TEMPLATES, x_vars + y_vars)


def sbox_weight_clauses_compact(x_vars, y_vars, act_var, hvy_var):
    """CNF clauses encoding DDT validity and weight variables for one S-box.

    Args:
        x_vars: list of 4 SAT variable indices for the input nibble bits.
        y_vars: list of 4 SAT variable indices for the output nibble bits.
        act_var: SAT variable index for the active flag (1 iff input diff != 0).
        hvy_var: SAT variable index for the heavy flag (1 iff DDT value = 2).
    """
    return _apply_templates(_SBOX_WEIGHT_TEMPLATES, x_vars + y_vars + [act_var, hvy_var])


def _active_clauses(cnf, R, r, s):
    """Add clauses linking active_var(R, r, s) to (input diff != 0) for S-box s.

    Args:
        cnf: the CNF formula to extend.
        R: total number of rounds.
        r: round index.
        s: S-box index (0-15).
    """
    a = active_var(R, r, s)
    x_bits = [diff_var(r, 4 * s + j) for j in range(4)]
    cnf.append([-a] + x_bits)
    for xi in x_bits:
        cnf.append([-xi, a])


def build_model(R):
    """Build a SAT model for R-round PRESENT differential trails (active S-box count only).

    Encodes S-box DDT constraints, the permutation layer, and forces
    both input and output differences to be non-zero.

    Args:
        R: number of rounds.
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
    cnf.append([diff_var(R, i) for i in range(64)])
    return cnf


def _weight_lits_weights(R, r_start, r_end):
    """Return (lits, weights) for a pseudo-Boolean constraint over rounds r_start..r_end-1.

    Each S-box contributes two literals: active_var with weight 2, heavy_var with weight 1,
    so the total encodes weight = 2*active + heavy.

    Args:
        R: total number of rounds (for variable numbering).
        r_start: first round index (inclusive).
        r_end: last round index (exclusive).
    """
    lits = []
    weights = []
    for r in range(r_start, r_end):
        for s in range(16):
            lits.append(active_var(R, r, s))
            lits.append(heavy_var(R, r, s))
            weights.append(2)
            weights.append(1)
    return lits, weights


def build_weighted_model(R, W=None):
    """Build a SAT model for R-round PRESENT differential trails with weight tracking.

    Uses the 10-bit prime implicant encoding so each clause jointly encodes
    DDT validity and the active/heavy weight variables.

    Args:
        R: number of rounds.
        W: optional upper bound on total trail weight added as a hard constraint.
           If None, no weight constraint is added (useful for incremental solving).
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
    cnf.append([diff_var(R, i) for i in range(64)])
    if W is not None:
        lits, ws = _weight_lits_weights(R, 0, R)
        cnf.extend(PBEnc.atmost(lits=lits, weights=ws, bound=W, top_id=cnf.nv).clauses)
    return cnf


def decode_trail(model, R):
    """Decode R+1 difference words from a SAT solver model.

    Args:
        model: list of signed integers from the solver (positive = True, negative = False).
        R: number of rounds.

    Returns:
        List of R+1 integers where entry r is the 64-bit difference word entering round r.
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

def trail_weight(trail):
    """Compute the exact weight of a differential trail.

    Inverts the permutation layer to recover each S-box output difference, then
    sums -log2(DDT[a][b] / 16) over all active S-boxes. Returns None if any
    transition is DDT-invalid (count == 0).

    Args:
        trail: list of R+1 64-bit difference words as returned by decode_trail.
    """
    total = 0
    for r in range(len(trail) - 1):
        d_in = trail[r]
        d_out = trail[r + 1]
        sbox_out = 0
        for i in range(64):
            if (d_out >> P[i]) & 1:
                sbox_out |= 1 << i

        for s in range(16):
            a = (d_in >> (4 * s)) & 0xF
            b = (sbox_out >> (4 * s)) & 0xF
            count = DDT[a][b]
            if count == 0:
                return None
            if a == 0:
                continue
            total += -log2(count / 16)

    return total


def trail_active_sboxes(trail):
    """Count the total number of active S-boxes across all rounds of a trail.

    Args:
        trail: list of R+1 64-bit difference words as returned by decode_trail.
    """
    total = 0
    for r in range(len(trail) - 1):
        d_in = trail[r]
        for s in range(16):
            if (d_in >> (4 * s)) & 0xF:
                total += 1
    return total