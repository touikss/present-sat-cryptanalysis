from pysat.formula import CNF
from pysat.pb import PBEnc

from .present import P, DDT


def _compute_pi_clauses(valid, invalid, nbits):
    # Quine-McCluskey: build prime implicants covering only invalid minterms
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
    # bits 0-3 = input diff, 4-7 = output diff, 8 = active, 9 = heavy
    # weight per S-box = 2*active + heavy
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
    return 1 + r * 64 + i


def active_var(R, r, s):
    return 1 + 64 * (R + 1) + r * 16 + s


def heavy_var(R, r, s):
    return 1 + 64 * (R + 1) + R * 16 + r * 16 + s


def sbox_clauses_compact(x_vars, y_vars):
    all_vars = x_vars + y_vars
    clauses = []
    for template in _SBOX_PI_TEMPLATES:
        clause = []
        for bit_index, is_positive in template:
            var = all_vars[bit_index]
            clause.append(var if is_positive else -var)
        clauses.append(clause)
    return clauses


def sbox_weight_clauses_compact(x_vars, y_vars, act_var, hvy_var):
    all_vars = x_vars + y_vars + [act_var, hvy_var]
    clauses = []
    for template in _SBOX_WEIGHT_TEMPLATES:
        clause = []
        for bit_index, is_positive in template:
            var = all_vars[bit_index]
            clause.append(var if is_positive else -var)
        clauses.append(clause)
    return clauses


def _active_clauses(cnf, R, r, s):
    a = active_var(R, r, s)
    x_bits = [diff_var(r, 4 * s + j) for j in range(4)]
    cnf.append([-a] + x_bits)
    for xi in x_bits:
        cnf.append([-xi, a])


def build_model(R):
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
    pos = set(model)
    diffs = []
    for r in range(R + 1):
        val = 0
        for i in range(64):
            if diff_var(r, i) in pos:
                val |= (1 << i)
        diffs.append(val)
    return diffs
