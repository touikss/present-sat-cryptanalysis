from pysat.solvers import Cadical195 as Cadical153
from pysat.card import CardEnc, EncType
from pysat.pb import PBEnc

from .encoding import (
    active_var,
    build_model, build_weighted_model,
    _weight_lits_weights,
)

ACTIVE_BOUNDS = {1:1, 2:2, 3:4, 4:6, 5:10, 6:12, 7:14, 8:16, 9:18, 10:20}


def find_min_active(R, use_bounds=False):
    """Find the minimum number of active S-boxes in any R-round differential trail."""
    bounds = ACTIVE_BOUNDS if use_bounds else None
    base   = build_model(R, active_bounds=bounds)
    lits   = [active_var(R, r, s) for r in range(R) for s in range(16)]
    with Cadical153(bootstrap_with=base.clauses) as solver:
        top = base.nv
        lo, hi = 1, len(lits)
        while lo < hi:
            mid  = (lo + hi) // 2
            top += 1
            act  = top
            enc  = CardEnc.atmost(lits=lits, bound=mid, top_id=top,
                                   encoding=EncType.seqcounter)
            for clause in enc.clauses:
                solver.add_clause([-act] + clause)
            top = enc.nv
            if solver.solve(assumptions=[act]):
                hi = mid
            else:
                lo = mid + 1
    return lo


def find_min_weight(R, W_max=None, use_bounds=False, weight_bounds=None):
    """Find the minimum differential trail weight for R rounds.

    Uses linear incremental search starting from 2*min_active, keeping the
    solver alive to reuse learned clauses between iterations.
    Weight per S-box = 2*active + heavy.
    """
    min_k = find_min_active(R, use_bounds=use_bounds)
    lo    = 2 * min_k
    hi    = W_max if W_max is not None else 3 * min_k

    abounds = ACTIVE_BOUNDS if use_bounds else None
    base    = build_weighted_model(R, W=None, active_bounds=abounds,
                                   weight_bounds=weight_bounds)
    pb_lits, pb_ws = _weight_lits_weights(R, 0, R)

    with Cadical153(bootstrap_with=base.clauses) as solver:
        top = base.nv
        for W in range(lo, hi + 1):
            top += 1
            act  = top
            pb   = PBEnc.atmost(lits=pb_lits, weights=pb_ws, bound=W, top_id=top)
            for clause in pb.clauses:
                solver.add_clause([-act] + clause)
            top = pb.nv
            if solver.solve(assumptions=[act]):
                return W

    return hi


def collect_weight_bounds(up_to, use_bounds=False):
    """Compute B[r] = min trail weight for r=1..up_to, each reusing prior results."""
    B = {}
    for r in range(1, up_to + 1):
        B[r] = find_min_weight(r, use_bounds=use_bounds,
                               weight_bounds=B if B else None)
    return B
