import argparse
import os
import signal
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from .search import find_min_active_sbox, find_min_trail_weight, ACTIVE_BOUNDS, SOLVERS


# ---------------------------------------------------------------------------
# Workers (run in child processes)
# ---------------------------------------------------------------------------

def _run_active(args: tuple[int, bool, str]) -> tuple[int, int, None, float]:
    r, use_bounds, solver = args
    t0 = time.time()
    a = find_min_active_sbox(r, use_bounds=use_bounds, solver=solver)
    return r, a, None, time.time() - t0


def _run_weight(args: tuple[int, bool, dict[int, int], str]) -> tuple[int, None, int, float]:
    r, use_bounds, wb, solver = args
    t0 = time.time()
    w = find_min_trail_weight(r, use_bounds=use_bounds, weight_bounds=wb, solver=solver)
    return r, None, w, time.time() - t0


def _run_active_weight(args: tuple[int, bool, dict[int, int], str]) -> tuple[int, int, int, float]:
    r, use_bounds, wb, solver = args
    t0 = time.time()
    a = find_min_active_sbox(r, use_bounds=use_bounds, solver=solver)
    w = find_min_trail_weight(r, use_bounds=use_bounds, weight_bounds=wb, solver=solver)
    return r, a, w, time.time() - t0


def _run_active_trail(args: tuple[int, bool, str]) -> tuple[int, int, list[int], float]:
    r, use_bounds, solver = args
    t0 = time.time()
    a, trail = find_min_active_sbox(r, use_bounds=use_bounds, solver=solver, return_trail=True)
    return r, a, trail, time.time() - t0


def _run_weight_trail(args: tuple[int, bool, dict[int, int], str]) -> tuple[int, int, list[int], float]:
    r, use_bounds, wb, solver = args
    t0 = time.time()
    w, trail = find_min_trail_weight(r, use_bounds=use_bounds, weight_bounds=wb, solver=solver, return_trail=True)
    return r, w, trail, time.time() - t0


def _run_active_weight_trail(args: tuple[int, bool, dict[int, int], str]) -> tuple[int, int, int, list[int], float]:
    r, use_bounds, wb, solver = args
    t0 = time.time()
    a = find_min_active_sbox(r, use_bounds=use_bounds, solver=solver)
    w, trail = find_min_trail_weight(r, use_bounds=use_bounds, weight_bounds=wb, solver=solver, return_trail=True)
    return r, a, w, trail, time.time() - t0


# ---------------------------------------------------------------------------
# Signal handling
# ---------------------------------------------------------------------------

def _shutdown(ex: ProcessPoolExecutor) -> None:
    print("\nInterrupted, shutting down workers...")
    procs = list(ex._processes.values()) if ex._processes else []
    ex.shutdown(wait=False, cancel_futures=True)
    for proc in procs:
        proc.terminate()
    sys.exit(1)


def _collect(ex: ProcessPoolExecutor, futures: dict):
    signal.signal(signal.SIGTERM, lambda _sig, _frame: _shutdown(ex))
    try:
        for fut in as_completed(futures):
            yield fut.result()
    except KeyboardInterrupt:
        _shutdown(ex)


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def _print_trail(r: int, trail: list[int]) -> None:
    print(f"R={r:2d}:")
    for i, delta in enumerate(trail):
        print(f"  Δ{i} = {delta:#018x}")


def _print_table(rounds, active: dict, weight: dict, times: dict, want_active: bool, want_weight: bool) -> None:
    if want_active and want_weight:
        print(f"{'R':>3}  {'min_active':>10}  {'2*active':>8}  {'min_weight':>10}  {'gap':>4}  {'time':>8}")
        print('-' * 54)
        for r in sorted(rounds):
            a, w = active[r], weight[r]
            gap = w - 2 * a
            marker = ' <--' if gap > 0 else ''
            print(f"{r:>3}  {a:>10}  {2*a:>8}  {w:>10}  {gap:>4}  {times[r]:>7.3f}s{marker}")
    elif want_active:
        print(f"{'R':>3}  {'min_active':>10}  {'time':>8}")
        print('-' * 26)
        for r in sorted(rounds):
            print(f"{r:>3}  {active[r]:>10}  {times[r]:>7.3f}s")
    else:
        print(f"{'R':>3}  {'min_weight':>10}  {'time':>8}")
        print('-' * 26)
        for r in sorted(rounds):
            print(f"{r:>3}  {weight[r]:>10}  {times[r]:>7.3f}s")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """CLI entry point for PRESENT differential trail search."""
    parser = argparse.ArgumentParser(description='PRESENT differential trail search')
    parser.add_argument('--rmin',    type=int, default=1)
    parser.add_argument('--rmax',    type=int, default=10)
    parser.add_argument('--bounds',  action='store_true',
                        help='use precomputed active-sbox prefix bounds to prune the search')
    parser.add_argument('--active',  action='store_true',
                        help='compute the minimum number of active S-boxes per round')
    parser.add_argument('--weight',  action='store_true',
                        help='compute the minimum trail weight per round')
    parser.add_argument('--trail',   action='store_true',
                        help='extract and display an optimal differential trail per round')
    parser.add_argument('--workers', type=int, default=None,
                        help='maximum number of parallel workers (default: cpu_count // 3)')
    parser.add_argument('--solver',  choices=list(SOLVERS), default='cadical',
                        help='SAT solver to use (default: cadical)')
    args = parser.parse_args()

    if not (args.active or args.weight or args.trail):
        parser.error('at least one of --active, --weight, --trail is required')

    rounds = list(range(args.rmin, args.rmax + 1))
    default_workers = max(1, os.cpu_count() // 3)
    n_workers = max(1, min(len(rounds), args.workers or default_workers))

    wb: dict[int, int] = {r: 2 * v for r, v in ACTIVE_BOUNDS.items()}

    active_res: dict[int, int] = {}
    weight_res: dict[int, int] = {}
    trail_res:  dict[int, list[int]] = {}
    times:      dict[int, float] = {}

    # Pick the worker that does the minimum necessary computation.
    if args.trail and args.active and args.weight:
        worker, worker_args = _run_active_weight_trail, [(r, args.bounds, wb, args.solver) for r in rounds]
        def unpack(res):
            r, a, w, trail, elapsed = res
            active_res[r] = a; weight_res[r] = w; trail_res[r] = trail; times[r] = elapsed
    elif args.trail and args.weight:
        worker, worker_args = _run_weight_trail, [(r, args.bounds, wb, args.solver) for r in rounds]
        def unpack(res):
            r, w, trail, elapsed = res
            weight_res[r] = w; trail_res[r] = trail; times[r] = elapsed
    elif args.trail and args.active:
        worker, worker_args = _run_active_trail, [(r, args.bounds, args.solver) for r in rounds]
        def unpack(res):
            r, a, trail, elapsed = res
            active_res[r] = a; trail_res[r] = trail; times[r] = elapsed
    elif args.trail:
        # trail alone → optimise weight
        worker, worker_args = _run_weight_trail, [(r, args.bounds, wb, args.solver) for r in rounds]
        def unpack(res):
            r, w, trail, elapsed = res
            weight_res[r] = w; trail_res[r] = trail; times[r] = elapsed
    elif args.active and args.weight:
        worker, worker_args = _run_active_weight, [(r, args.bounds, wb, args.solver) for r in rounds]
        def unpack(res):
            r, a, w, elapsed = res
            active_res[r] = a; weight_res[r] = w; times[r] = elapsed
    elif args.weight:
        worker, worker_args = _run_weight, [(r, args.bounds, wb, args.solver) for r in rounds]
        def unpack(res):
            r, _, w, elapsed = res
            weight_res[r] = w; times[r] = elapsed
    else:  # active only
        worker, worker_args = _run_active, [(r, args.bounds, args.solver) for r in rounds]
        def unpack(res):
            r, a, _, elapsed = res
            active_res[r] = a; times[r] = elapsed

    with ProcessPoolExecutor(max_workers=n_workers) as ex:
        futures = {ex.submit(worker, a): a[0] for a in worker_args}
        for res in _collect(ex, futures):
            unpack(res)

    # Table
    if args.active or args.weight:
        print()
        _print_table(rounds, active_res, weight_res, times,
                     want_active=args.active, want_weight=args.weight)

    # Trails
    if args.trail:
        print()
        for r in sorted(trail_res):
            _print_trail(r, trail_res[r])
            print()


if __name__ == '__main__':
    main()
