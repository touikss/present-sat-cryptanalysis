from pysat.formula import CNF
from pysat.card import CardEnc, EncType
from pysat.pb import PBEnc

from .present import P, DDT


def diff_var(r, i):
    """Return the SAT variable for bit i of the difference word at round r."""
    return 1 + r * 64 + i


def active_var(R, r, s):
    """Return the SAT variable for the active flag of S-box s at round r."""
    return 1 + 64 * (R + 1) + r * 16 + s


def w2_var(R, r, s):
    """Return the SAT variable encoding a weight-2 contribution for S-box s at round r.

    Shares the same index as active_var; in the weighted model an active S-box
    contributes weight 2 unless w3_var forces the heavier branch.
    """
    return 1 + 64 * (R + 1) + r * 16 + s


def w3_var(R, r, s):
    """Return the SAT variable encoding a weight-3 contribution for S-box s at round r."""
    return 1 + 64 * (R + 1) + R * 16 + r * 16 + s


def forbid_assignment(x_vars, y_vars, x_val, y_val):
    """Build a clause that forbids the specific (x_val, y_val) assignment on (x_vars, y_vars)."""
    clause = []
    for i, var in enumerate(x_vars):
        clause.append(-var if (x_val >> i) & 1 else var)
    for i, var in enumerate(y_vars):
        clause.append(-var if (y_val >> i) & 1 else var)
    return clause


def sbox_clauses(x_vars, y_vars, ddt):
    """Return clauses ruling out all (input, output) pairs with zero DDT probability."""
    return [
        forbid_assignment(x_vars, y_vars, a, b)
        for a in range(16)
        for b in range(16)
        if ddt[a][b] == 0
    ]


def build_round(cnf, r):
    """Add CNF clauses encoding the S-box and permutation layer for round r."""
    for s in range(16):
        x_vars = [diff_var(r,   4 * s + j) for j in range(4)]
        y_vars = [diff_var(r+1, P[4 * s + j]) for j in range(4)]
        for clause in sbox_clauses(x_vars, y_vars, DDT):
            cnf.append(clause)


def active_clauses(cnf, R, r, s):
    """Add clauses linking active_var(r, s) to the non-zero condition on S-box s at round r."""
    a = active_var(R, r, s)
    x = [diff_var(r, 4 * s + j) for j in range(4)]
    cnf.append([-a] + x)
    for xi in x:
        cnf.append([-xi, a])


def build_model(R):
    """Build the base SAT model for an R-round PRESENT differential trail (active S-box count)."""
    cnf = CNF()
    for r in range(R):
        build_round(cnf, r)
        for s in range(16):
            active_clauses(cnf, R, r, s)
    cnf.append([diff_var(0, i) for i in range(64)])
    return cnf


def weight_clauses(cnf, R, r, s):
    """Add clauses that encode the differential weight (2 or 3) for S-box s at round r."""
    x_vars = [diff_var(r,   4 * s + j) for j in range(4)]
    y_vars = [diff_var(r+1, P[4 * s + j]) for j in range(4)]
    w2 = w2_var(R, r, s)
    w3 = w3_var(R, r, s)
    for a in range(16):
        for b in range(16):
            if DDT[a][b] == 0:
                continue
            c2 = forbid_assignment(x_vars, y_vars, a, b)
            c2.append(w2 if DDT[a][b] == 4 else -w2)
            cnf.append(c2)
            c3 = forbid_assignment(x_vars, y_vars, a, b)
            c3.append(w3 if DDT[a][b] == 2 else -w3)
            cnf.append(c3)


def build_weighted_model(R, W=None):
    """Build the weighted SAT model for R rounds, optionally bounding total weight by W."""
    cnf = CNF()
    for r in range(R):
        build_round(cnf, r)
        for s in range(16):
            weight_clauses(cnf, R, r, s)
    cnf.append([diff_var(0, i) for i in range(64)])
    if W is not None:
        lits = []
        ws   = []
        for r in range(R):
            for s in range(16):
                lits += [w2_var(R, r, s), w3_var(R, r, s)]
                ws   += [2, 3]
        cnf.extend(PBEnc.atmost(lits=lits, weights=ws, bound=W, top_id=cnf.nv).clauses)
    return cnf
