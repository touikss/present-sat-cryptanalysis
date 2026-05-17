from concurrent.futures import ProcessPoolExecutor, FIRST_COMPLETED, wait as fut_wait

from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.pb import PBEnc

from .encoding import (
    active_var, w2_var, w3_var,
    build_model, build_weighted_model,
)


def portfolio_solve(args):
    """Solve a CNF instance with the specified solver; returns True if satisfiable."""
    from pysat.solvers import Cadical153, Glucose4, Glucose42
    clauses, solver_name = args
    cls = {'cadical153': Cadical153, 'glucose4': Glucose4, 'glucose42': Glucose42}[solver_name]
    with cls(bootstrap_with=clauses) as s:
        return s.solve()


def find_min_active(R):
    """Find the minimum number of active S-boxes in any R-round PRESENT differential trail."""
    base = build_model(R)
    lits = [active_var(R, r, s) for r in range(R) for s in range(16)]
    with Cadical153(bootstrap_with=base.clauses) as solver:
        top = base.nv
        lo, hi = 1, len(lits)
        while lo < hi:
            mid = (lo + hi) // 2
            top += 1
            act = top
            enc = CardEnc.atmost(lits=lits, bound=mid, top_id=top,
                                  encoding=EncType.seqcounter)
            for clause in enc.clauses:
                solver.add_clause([-act] + clause)
            top = enc.nv
            if solver.solve(assumptions=[act]):
                hi = mid
            else:
                lo = mid + 1
    return lo


def find_min_weight_fast(R, W_max=None, n_portfolio=3):
    """Find the minimum differential trail weight for R rounds using binary search and a solver portfolio."""
    min_k = find_min_active(R)
    lo = 2 * min_k
    hi = W_max if W_max is not None else 3 * min_k

    base = build_weighted_model(R, W=None)
    pb_lits = []
    pb_ws   = []
    for r in range(R):
        for s in range(16):
            pb_lits += [w2_var(R, r, s), w3_var(R, r, s)]
            pb_ws   += [2, 3]

    w3_false    = [[-w3_var(R, r, s)] for r in range(R) for s in range(16)]
    pb_tight    = PBEnc.atmost(lits=pb_lits, weights=pb_ws, bound=lo, top_id=base.nv).clauses
    opt_clauses = base.clauses + pb_tight + w3_false

    if n_portfolio > 1:
        names = ['cadical153', 'glucose4', 'glucose42'][:n_portfolio]
        with ProcessPoolExecutor(max_workers=n_portfolio) as ex:
            futs = [ex.submit(portfolio_solve, (opt_clauses, nm)) for nm in names]
            done, _ = fut_wait(futs, return_when=FIRST_COMPLETED)
            sat = list(done)[0].result()
    else:
        with Cadical153(bootstrap_with=opt_clauses) as s:
            sat = s.solve()

    if sat:
        return lo

    lo += 1

    with Cadical153(bootstrap_with=base.clauses) as solver:
        top    = base.nv
        phases = None
        while lo < hi:
            mid = (lo + hi) // 2
            top += 1
            act = top
            pb  = PBEnc.atmost(lits=pb_lits, weights=pb_ws, bound=mid, top_id=top)
            for clause in pb.clauses:
                solver.add_clause([-act] + clause)
            top = pb.nv
            if phases:
                solver.set_phases(phases)
            if solver.solve(assumptions=[act]):
                phases = solver.get_model()
                hi = mid
            else:
                lo = mid + 1
    return lo
