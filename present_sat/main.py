import argparse
import os
import signal
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from .search import find_min_active, find_min_weight, ACTIVE_BOUNDS, SOLVERS


def _run_active(args: tuple[int, bool, str]) -> tuple[int, int, float]:
    """Worker: run active S-box search for R rounds, return (r, min_active, elapsed).

    Args:
        args: tuple of (R, use_bounds, solver).
    """
    r, use_bounds, solver = args
    t0 = time.time()
    a = find_min_active(r, use_bounds=use_bounds, solver=solver)
    return r, a, time.time() - t0


def _run_weight(args: tuple[int, bool, dict[int, int], str]) -> tuple[int, int, float]:
    """Worker: run min-weight search for R rounds, return (r, weight, elapsed).

    Args:
        args: tuple of (R, use_bounds, weight_bounds, solver).
    """
    r, use_bounds, wb, solver = args
    t0 = time.time()
    w = find_min_weight(r, use_bounds=use_bounds, weight_bounds=wb, solver=solver)
    return r, w, time.time() - t0


def _shutdown(ex: ProcessPoolExecutor) -> None:
    """Terminate all worker processes and exit.

    Args:
        ex: the executor whose workers should be terminated.
    """
    print("\nInterrupted, shutting down workers...")
    procs = list(ex._processes.values()) if ex._processes else []
    ex.shutdown(wait=False, cancel_futures=True)
    for proc in procs:
        proc.terminate()
    sys.exit(1)


def _collect(ex: ProcessPoolExecutor, futures: dict):
    """Yield results from futures as they complete, with clean shutdown on SIGINT/SIGTERM.

    Args:
        ex: the executor running the futures.
        futures: dict mapping future -> round index.
    """
    signal.signal(signal.SIGTERM, lambda _sig, _frame: _shutdown(ex))
    try:
        for fut in as_completed(futures):
            yield fut.result()
    except KeyboardInterrupt:
        _shutdown(ex)


def main() -> None:
    """CLI entry point for PRESENT differential trail search."""
    parser = argparse.ArgumentParser(description='PRESENT differential trail search')
    parser.add_argument('--rmin',        type=int, default=1)
    parser.add_argument('--rmax',        type=int, default=10)
    parser.add_argument('--bounds',      action='store_true',
                        help='use precomputed active-sbox prefix bounds to prune the search')
    parser.add_argument('--active-only', action='store_true',
                        help='only compute the minimum number of active S-boxes (skip weight search)')
    parser.add_argument('--workers',     type=int, default=None,
                        help='maximum number of parallel workers (default: cpu_count // 3)')
    parser.add_argument('--solver',      choices=list(SOLVERS), default='cadical',
                        help='SAT solver to use (default: cadical)')
    args = parser.parse_args()

    rounds = list(range(args.rmin, args.rmax + 1))
    results: dict[int, int] = {}
    times: dict[int, float] = {}

    default_workers = max(1, os.cpu_count() // 3)
    n_workers = max(1, min(len(rounds), args.workers if args.workers else default_workers))

    if args.active_only:
        with ProcessPoolExecutor(max_workers=n_workers) as ex:
            futures = {ex.submit(_run_active, (r, args.bounds, args.solver)): r for r in rounds}
            for r, a, elapsed in _collect(ex, futures):
                results[r] = a
                times[r] = elapsed
                print(f"R={r:2d}  min_active={a:3d}  {elapsed:.3f}s")

        print()
        print(f"{'R':>3}  {'min_active':>10}  {'time':>8}")
        print('-' * 26)
        for r in sorted(results):
            print(f"{r:>3}  {results[r]:>10}  {times[r]:>7.3f}s")
    else:
        wb: dict[int, int] = {r: 2 * v for r, v in ACTIVE_BOUNDS.items()}

        with ProcessPoolExecutor(max_workers=n_workers) as ex:
            futures = {ex.submit(_run_weight, (r, args.bounds, wb, args.solver)): r for r in rounds}
            for r, w, elapsed in _collect(ex, futures):
                results[r] = w
                times[r] = elapsed
                print(f"R={r:2d}  weight={w:3d}  {elapsed:.3f}s")

        print()
        print(f"{'R':>3}  {'min_active':>10}  {'2*active':>8}  {'min_weight':>10}  {'gap':>4}")
        print('-' * 44)
        for r in sorted(results):
            a = find_min_active(r, use_bounds=args.bounds, solver=args.solver)
            w = results[r]
            gap = w - 2 * a
            marker = ' <--' if gap > 0 else ''
            print(f"{r:>3}  {a:>10}  {2*a:>8}  {w:>10}  {gap:>4}{marker}")


if __name__ == '__main__':
    main()
