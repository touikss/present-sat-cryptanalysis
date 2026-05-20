from pysat.solvers import Cadical195, Kissat404
from pysat.card import CardEnc, EncType
from pysat.pb import PBEnc

from .encoding import active_var, build_model, build_weighted_model, _weight_lits_weights, decode_trail

# Known minimum active S-box counts for PRESENT (from the literature).
ACTIVE_BOUNDS = {
    1: 1,   2: 2,   3: 4,   4: 6,   5: 10,  6: 12,  7: 14,  8: 16,  9: 18,  10: 20,
    11: 22, 12: 24, 13: 26, 14: 28, 15: 30, 16: 32, 17: 34, 18: 36, 19: 38, 20: 40,
    21: 42, 22: 44, 23: 46, 24: 48, 25: 50, 26: 52, 27: 54, 28: 56, 29: 58, 30: 60,
    31: 62,
}

# Known minimum trail weights for PRESENT (from the literature).
# Used as a lower bound: weight[R] >= WEIGHT_BOUNDS[R-1] + 2.
WEIGHT_BOUNDS = {
    1: 2, 2: 4, 3: 8, 4: 12, 5: 20, 6: 24,  7: 28,  8: 32,  9: 36,  10: 41,
    11: 46, 12: 52, 13: 56, 14: 62, 15: 66, 16: 70, 17: 74, 18: 78, 19: 82, 20: 86,
    21: 90, 22: 96, 23: 100, 24: 106, 25: 110, 26: 116, 27: 120, 28: 124, 29: 128,
    30: 132, 31: 136,
}

SOLVERS = {
    "cadical": Cadical195,
    "kissat": Kissat404,
}


def find_min_active_sbox(R, solver="kissat", *, return_trail=False):
    """Find the minimum number of active S-boxes in any R-round differential trail.

    Uses binary search with a cardinality constraint (at-most k active S-boxes).
    CaDiCaL reuses learned clauses across iterations; Kissat creates a fresh solver each time.
    Returns the cached value from ACTIVE_BOUNDS when available and return_trail is False.

    Args:
        R: number of rounds.
        solver: SAT solver to use, either 'cadical' or 'kissat'.
        return_trail: if True, also return an optimal trail as a list of R+1 difference words.
    """
    base = build_model(R)
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
            if not return_trail:
                return lo
            top += 1
            act = top
            enc = CardEnc.atmost(lits=lits, bound=lo, top_id=top, encoding=EncType.seqcounter)
            for clause in enc.clauses:
                s.add_clause([-act] + clause)
            s.solve(assumptions=[act])
            return lo, decode_trail(s.get_model(), R)
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
        if not return_trail:
            return lo
        enc = CardEnc.atmost(lits=lits, bound=lo, top_id=base.nv, encoding=EncType.seqcounter)
        with Kissat404(bootstrap_with=base.clauses + enc.clauses) as s:
            s.solve()
            return lo, decode_trail(s.get_model(), R)


def find_min_trail_weight(R, W_min=None, solver="kissat", *, return_trail=False, progress_queue=None):
    """Find the minimum differential trail weight for R rounds.

    First computes min_active, then does a linear search from lo upward.
    CaDiCaL keeps the solver alive between iterations to reuse learned clauses.
    Kissat creates a fresh solver for each candidate weight.

    Args:
        R: number of rounds.
        W_min: optional lower bound (e.g. weight[R-1] from a previous run).
               WEIGHT_BOUNDS[R-1] is used as fallback when W_min is None.
        solver: SAT solver to use, either 'cadical' or 'kissat'.
        return_trail: if True, also return an optimal trail as a list of R+1 difference words.
        progress_queue: optional multiprocessing.Queue to send (R, W) progress updates.
    """
    min_k = ACTIVE_BOUNDS[R] if R in ACTIVE_BOUNDS else find_min_active_sbox(R, solver=solver)

    # output diff is non-zero, so adding a round adds at least weight 2
    # => weight[R] >= weight[R-1] + 2, use WEIGHT_BOUNDS as fallback when W_min not given
    prev = W_min if W_min is not None else WEIGHT_BOUNDS.get(R - 1)
    lo = max(2 * min_k, prev + 2) if prev is not None else 2 * min_k
    hi = max(3 * min_k, lo + 16)

    if solver == "cadical":
        base = build_weighted_model(R, W=None)
        pb_lits, pb_ws = _weight_lits_weights(R, 0, R)
        with Cadical195(bootstrap_with=base.clauses) as s:
            top = base.nv
            for W in range(lo, hi + 1):
                if progress_queue is not None:
                    progress_queue.put((R, W))
                top += 1
                act = top
                pb = PBEnc.atmost(lits=pb_lits, weights=pb_ws, bound=W, top_id=top)
                for clause in pb.clauses:
                    s.add_clause([-act] + clause)
                top = pb.nv
                if s.solve(assumptions=[act]):
                    return (W, decode_trail(s.get_model(), R)) if return_trail else W
    else:
        for W in range(lo, hi + 1):
            if progress_queue is not None:
                progress_queue.put((R, W))
            base = build_weighted_model(R, W=W)
            with Kissat404(bootstrap_with=base.clauses) as s:
                if s.solve():
                    return (W, decode_trail(s.get_model(), R)) if return_trail else W

    return (hi, []) if return_trail else hi
