from pysat.formula import CNF
from pysat.card import CardEnc, EncType
from pysat.pb import PBEnc

from .present import P, DDT


def diff_var(r, i):
    return 1 + r * 64 + i


def active_var(R, r, s):
    return 1 + 64 * (R + 1) + r * 16 + s


def w2_var(R, r, s):
    return 1 + 64 * (R + 1) + r * 16 + s


def w3_var(R, r, s):
    return 1 + 64 * (R + 1) + R * 16 + r * 16 + s


def forbid_assignment(x_vars, y_vars, x_val, y_val):
    clause = []
    for i, var in enumerate(x_vars):
        clause.append(-var if (x_val >> i) & 1 else var)
    for i, var in enumerate(y_vars):
        clause.append(-var if (y_val >> i) & 1 else var)
    return clause


def sbox_clauses(x_vars, y_vars, ddt):
    return [
        forbid_assignment(x_vars, y_vars, a, b)
        for a in range(16)
        for b in range(16)
        if ddt[a][b] == 0
    ]


def build_round(cnf, r):
    for s in range(16):
        x_vars = [diff_var(r,   4 * s + j) for j in range(4)]
        y_vars = [diff_var(r+1, P[4 * s + j]) for j in range(4)]
        for clause in sbox_clauses(x_vars, y_vars, DDT):
            cnf.append(clause)


def active_clauses(cnf, R, r, s):
    a = active_var(R, r, s)
    x = [diff_var(r, 4 * s + j) for j in range(4)]
    cnf.append([-a] + x)
    for xi in x:
        cnf.append([-xi, a])


def build_model(R):
    cnf = CNF()
    for r in range(R):
        build_round(cnf, r)
        for s in range(16):
            active_clauses(cnf, R, r, s)
    cnf.append([diff_var(0, i) for i in range(64)])
    return cnf


def weight_clauses(cnf, R, r, s):
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
