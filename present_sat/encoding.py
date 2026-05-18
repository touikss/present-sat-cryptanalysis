from pysat.formula import CNF
from pysat.card import CardEnc, EncType
from pysat.pb import PBEnc

from .present import P, DDT


def _compute_pi_clauses(valid, invalid, nbits):
    """Quine-McCluskey prime implicant cover on an nbits-wide boolean space.

    Returns clause templates: list of [(bit_index, is_positive_literal), ...].
    Each template encodes one prime implicant that covers only invalid minterms.
    """
    mask_all = (1 << nbits) - 1

    current = {(v, 0) for v in invalid}
    prime_implicants = set()

    while current:
        merged = set()
        used   = set()
        imps   = list(current)
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
                new_val  = v1 & ~diff & mask_all
                if not any((p & ~new_mask) == (new_val & ~new_mask) for p in valid):
                    merged.add((new_val, new_mask))
                    used.add(imps[i])
                    used.add(imps[j])
        prime_implicants |= current - used
        current = merged

    def covers(val, mask):
        return frozenset(p for p in invalid if (p & ~mask) == (val & ~mask))

    pi_cov    = [(pi, covers(*pi)) for pi in prime_implicants]
    uncovered = set(invalid)
    selected  = []
    while uncovered:
        pi_cov.sort(key=lambda x: len(x[1] & uncovered), reverse=True)
        selected.append(pi_cov[0][0])
        uncovered -= pi_cov[0][1]
        pi_cov = [(pi, cov) for pi, cov in pi_cov if cov & uncovered]

    return [
        [(i, not ((val >> i) & 1)) for i in range(nbits) if not (mask >> i) & 1]
        for val, mask in selected
    ]


def _compute_sbox_pi_clauses(ddt):
    """8-bit compact CNF covering invalid (input, output) DDT pairs."""
    valid   = frozenset(a | (b << 4) for a in range(16) for b in range(16) if ddt[a][b] > 0)
    invalid = frozenset(a | (b << 4) for a in range(16) for b in range(16) if ddt[a][b] == 0)
    return _compute_pi_clauses(valid, invalid, 8)


def _compute_sbox_weight_pi_clauses(ddt):
    """10-bit compact CNF for combined S-box validity + weight constraint.

    Bit layout: bits 0-3 = x (input), 4-7 = y (output), 8 = active, 9 = heavy.
    Valid minterms:
      - (0,0,active=0,heavy=0): inactive S-box
      - (a,b,active=1,heavy=0): weight-2 transition (DDT[a][b]=4)
      - (a,b,active=1,heavy=1): weight-3 transition (DDT[a][b]=2)
    Weight per S-box = 2*active + heavy.
    """
    valid = {0}  # inactive
    for a in range(1, 16):
        for b in range(16):
            if ddt[a][b] == 4:
                valid.add(a | (b << 4) | (1 << 8))
            elif ddt[a][b] == 2:
                valid.add(a | (b << 4) | (1 << 8) | (1 << 9))
    valid   = frozenset(valid)
    invalid = frozenset(v for v in range(1 << 10) if v not in valid)
    return _compute_pi_clauses(valid, invalid, 10)


_SBOX_PI_TEMPLATES     = _compute_sbox_pi_clauses(DDT)
_SBOX_WEIGHT_TEMPLATES = _compute_sbox_weight_pi_clauses(DDT)


def diff_var(r, i):
    """SAT variable for bit i of the difference word at round r."""
    return 1 + r * 64 + i


def active_var(R, r, s):
    """SAT variable: S-box s at round r is active (non-zero input difference)."""
    return 1 + 64 * (R + 1) + r * 16 + s


def w2_var(R, r, s):
    """Alias for active_var (kept for backward compatibility with find_min_active)."""
    return active_var(R, r, s)


def w3_var(R, r, s):
    """SAT variable: S-box s at round r has a weight-3 (heavy) transition."""
    return 1 + 64 * (R + 1) + R * 16 + r * 16 + s


def forbid_assignment(x_vars, y_vars, x_val, y_val):
    """Clause forbidding the specific (x_val, y_val) assignment on (x_vars, y_vars)."""
    clause = []
    for i, var in enumerate(x_vars):
        clause.append(-var if (x_val >> i) & 1 else var)
    for i, var in enumerate(y_vars):
        clause.append(-var if (y_val >> i) & 1 else var)
    return clause


def sbox_clauses(x_vars, y_vars, ddt):
    """Clauses ruling out all (input, output) DDT pairs with zero probability."""
    return [
        forbid_assignment(x_vars, y_vars, a, b)
        for a in range(16)
        for b in range(16)
        if ddt[a][b] == 0
    ]


def sbox_clauses_compact(x_vars, y_vars):
    """Compact clauses using precomputed 8-bit prime implicants (validity only)."""
    all_vars = x_vars + y_vars
    return [
        [all_vars[i] if pos else -all_vars[i] for i, pos in tmpl]
        for tmpl in _SBOX_PI_TEMPLATES
    ]


def sbox_weight_clauses_compact(x_vars, y_vars, act_var, hvy_var):
    """Compact clauses for combined S-box validity + weight (active, heavy) encoding.

    Uses precomputed 10-bit prime implicants. Encodes:
      - Which (x,y) transitions are DDT-valid
      - act_var = 1 iff S-box is active (x != 0)
      - hvy_var = 1 iff transition has weight 3 (DDT[x][y] = 2)
    Weight contribution = 2*act_var + hvy_var.
    """
    all_vars = x_vars + y_vars + [act_var, hvy_var]
    return [
        [all_vars[i] if pos else -all_vars[i] for i, pos in tmpl]
        for tmpl in _SBOX_WEIGHT_TEMPLATES
    ]


def build_round(cnf, r, compact=False):
    """Add CNF clauses for S-box and permutation layer at round r (validity only)."""
    for s in range(16):
        x_vars = [diff_var(r,   4 * s + j) for j in range(4)]
        y_vars = [diff_var(r+1, P[4 * s + j]) for j in range(4)]
        clauses = sbox_clauses_compact(x_vars, y_vars) if compact else sbox_clauses(x_vars, y_vars, DDT)
        for clause in clauses:
            cnf.append(clause)


def active_clauses(cnf, R, r, s):
    """Add clauses linking active_var(r, s) to (x != 0) for S-box s at round r."""
    a = active_var(R, r, s)
    x = [diff_var(r, 4 * s + j) for j in range(4)]
    cnf.append([-a] + x)
    for xi in x:
        cnf.append([-xi, a])


def build_model(R, active_bounds=None, compact=False):
    """SAT model for R-round PRESENT differential trail (active S-box count only)."""
    cnf = CNF()
    for r in range(R):
        build_round(cnf, r, compact=compact)
        for s in range(16):
            active_clauses(cnf, R, r, s)
    cnf.append([diff_var(0, i) for i in range(64)])
    if active_bounds:
        valid = {k: v for k, v in active_bounds.items() if k < R}
        if valid:
            k = max(valid)
            lits = [active_var(R, r, s) for r in range(k) for s in range(16)]
            cnf.extend(CardEnc.atleast(lits=lits, bound=valid[k],
                                       encoding=EncType.seqcounter, top_id=cnf.nv).clauses)
    return cnf


def _weight_lits_weights(R, r_start, r_end):
    """Return (lits, weights) for PBEnc covering S-boxes in rounds r_start..r_end-1.

    Weight per S-box = 2*active + 1*heavy, so weights alternate [2, 1, 2, 1, ...].
    """
    lits = []
    ws   = []
    for r in range(r_start, r_end):
        for s in range(16):
            lits += [active_var(R, r, s), w3_var(R, r, s)]
            ws   += [2, 1]
    return lits, ws


def build_weighted_model(R, W=None, active_bounds=None, compact=False, weight_bounds=None):
    """Build weighted SAT model using compact combined S-box+weight encoding.

    Uses 10-bit prime implicant templates: each template clause encodes both
    DDT validity and weight variable semantics in one compact representation.
    Weight = 2 * active_var + w3_var per S-box.
    """
    cnf = CNF()
    for r in range(R):
        for s in range(16):
            x_vars = [diff_var(r,   4 * s + j) for j in range(4)]
            y_vars = [diff_var(r+1, P[4 * s + j]) for j in range(4)]
            act = active_var(R, r, s)
            hvy = w3_var(R, r, s)
            for clause in sbox_weight_clauses_compact(x_vars, y_vars, act, hvy):
                cnf.append(clause)
    cnf.append([diff_var(0, i) for i in range(64)])

    if weight_bounds:
        # PC1: first `split` rounds ≥ B[split]. Cheap for small split (few lits, small bound).
        # PC2: last `R-split` rounds ≥ B[R-split]. Cheap when R-split is small.
        # Only use splits where the resulting PBEnc stays manageable.
        # Cheap PC1: split=1..4 (small prefix).
        for split in range(1, min(R, 5)):
            b_pre = weight_bounds.get(split, 0)
            if b_pre > 0:
                lits, ws = _weight_lits_weights(R, 0, split)
                cnf.extend(PBEnc.atleast(lits=lits, weights=ws, bound=b_pre,
                                         top_id=cnf.nv).clauses)
        # Cheap PC2: last 1..4 rounds form the suffix (split = R-4..R-1).
        for suf_len in range(1, min(R, 5)):
            split = R - suf_len
            b_suf = weight_bounds.get(suf_len, 0)
            if b_suf > 0:
                lits, ws = _weight_lits_weights(R, split, R)
                cnf.extend(PBEnc.atleast(lits=lits, weights=ws, bound=b_suf,
                                         top_id=cnf.nv).clauses)

    if active_bounds:
        valid = {k: v for k, v in active_bounds.items() if k < R}
        if valid:
            k = max(valid)
            lits = [active_var(R, r, s) for r in range(k) for s in range(16)]
            cnf.extend(CardEnc.atleast(lits=lits, bound=valid[k],
                                       encoding=EncType.seqcounter, top_id=cnf.nv).clauses)

    if W is not None:
        lits, ws = _weight_lits_weights(R, 0, R)
        cnf.extend(PBEnc.atmost(lits=lits, weights=ws, bound=W, top_id=cnf.nv).clauses)

    return cnf
