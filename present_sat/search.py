from typing import Any

from pysat.solvers import Cadical195, Kissat404
from pysat.card import CardEnc, EncType
from pysat.pb import PBEnc

from .encoding import active_var, build_model, build_weighted_model, _weight_lits_weights

ACTIVE_BOUNDS: dict[int, int] = {1: 1, 2: 2, 3: 4, 4: 6, 5: 10, 6: 12, 7: 14, 8: 16, 9: 18, 10: 20}

SOLVERS: dict[str, Any] = {
    "cadical": Cadical195,
    "kissat":  Kissat404,
}


def find_min_active(R: int, use_bounds: bool = False, solver: str = "cadical") -> int:
    """Find the minimum number of active S-boxes in any R-round differential trail.

    Args:
        R: number of rounds.
        use_bounds: if True, adds precomputed prefix active-sbox bounds to speed up search.
        solver: SAT solver to use, either 'cadical' or 'kissat'.
    """
    bounds = ACTIVE_BOUNDS if use_bounds else None
    base = build_model(R, active_bounds=bounds)
    lits = [active_var(R, r, s) for r in range(R) for s in range(16)]

    if solver == "cadical":
        with Cadical195(bootstrap_with=base.clauses) as s:
            top = base.nv
            lo, hi = 1, len(lits)
            while lo < hi:
                mid = (lo + hi) // 2
                top += 1
                act = top
                enc = CardEnc.atmost(lits=lits, bound=mid, top_id=top, encoding=EncType.seqcounter)
                for clause in enc.clauses:
                    s.add_clause([-act] + clause)
                top = enc.nv
                if s.solve(assumptions=[act]):
                    hi = mid
                else:
                    lo = mid + 1
        return lo
    else:
        lo, hi = 1, len(lits)
        while lo < hi:
            mid = (lo + hi) // 2
            enc = CardEnc.atmost(lits=lits, bound=mid, top_id=base.nv, encoding=EncType.seqcounter)
            cnf_clauses = base.clauses + enc.clauses
            with Kissat404(bootstrap_with=cnf_clauses) as s:
                sat = s.solve()
            if sat:
                hi = mid
            else:
                lo = mid + 1
        return lo


def find_min_weight(R: int, W_max: int | None = None,
                    use_bounds: bool = False,
                    weight_bounds: dict[int, int] | None = None,
                    solver: str = "cadical") -> int:
    """Find the minimum differential trail weight for R rounds.

    Uses linear incremental search starting from 2*min_active.
    With CaDiCaL, the solver is kept alive between iterations to reuse learned clauses.
    With Kissat, a fresh solver is created at each iteration (no assumption support).
    Weight per S-box = 2*active + heavy.

    Args:
        R: number of rounds.
        W_max: optional upper bound for the search (defaults to 3*min_active).
        use_bounds: if True, adds precomputed prefix active-sbox bounds.
        weight_bounds: optional dict mapping round count k to min trail weight,
                       used to add PC1/PC2 constraints to the model.
        solver: SAT solver to use, either 'cadical' or 'kissat'.
    """
    min_k = find_min_active(R, use_bounds=use_bounds, solver=solver)
    lo = 2 * min_k
    hi = W_max if W_max is not None else 3 * min_k

    abounds = ACTIVE_BOUNDS if use_bounds else None

    if solver == "cadical":
        base = build_weighted_model(R, W=None, active_bounds=abounds,
                                    weight_bounds=weight_bounds)
        pb_lits, pb_ws = _weight_lits_weights(R, 0, R)
        with Cadical195(bootstrap_with=base.clauses) as s:
            top = base.nv
            for W in range(lo, hi + 1):
                top += 1
                act = top
                pb = PBEnc.atmost(lits=pb_lits, weights=pb_ws, bound=W, top_id=top)
                for clause in pb.clauses:
                    s.add_clause([-act] + clause)
                top = pb.nv
                if s.solve(assumptions=[act]):
                    return W
    else:
        for W in range(lo, hi + 1):
            base = build_weighted_model(R, W=W, active_bounds=abounds,
                                        weight_bounds=weight_bounds)
            with Kissat404(bootstrap_with=base.clauses) as s:
                if s.solve():
                    return W

    return hi
