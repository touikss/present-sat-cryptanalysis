import argparse
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from .search import find_min_active, find_min_weight_fast, collect_weight_bounds, ACTIVE_BOUNDS
from .matsui import find_min_weight_matsui


def run_r(args):
    """Run the SAT min-weight search for R rounds and return (r, weight, elapsed_seconds)."""
    r, use_bounds, compact, wb = args
    t0 = time.time()
    w = find_min_weight_fast(r, use_bounds=use_bounds, compact=compact, weight_bounds=wb)
    return r, w, time.time() - t0


def main():
    """CLI entry point: search min-weight differential trails up to --rmax rounds in parallel."""
    parser = argparse.ArgumentParser(description='PRESENT min-weight differential trail search')
    parser.add_argument('--rmin', type=int, default=1)
    parser.add_argument('--rmax', type=int, default=10)
    parser.add_argument('--bounds', action='store_true',
                        help='use precomputed prefix bounds to prune the search (SAT only)')
    parser.add_argument('--compact', action='store_true',
                        help='use compact prime-implicant S-box encoding (SAT only)')
    parser.add_argument('--matsui', action='store_true',
                        help='use Matsui DFS instead of SAT (sequential, shares B table)')
    parser.add_argument('--pc', action='store_true',
                        help='add Matsui PC1/PC2 weight bounds as CNF constraints (SAT only)')
    args = parser.parse_args()

    rmin       = args.rmin
    rmax       = args.rmax
    use_bounds = args.bounds
    compact    = args.compact
    rounds     = list(range(rmin, rmax + 1))

    results = {}
    times   = {}

    if args.matsui:
        B = {0: 0}
        for r in rounds:
            t0 = time.time()
            w = find_min_weight_matsui(r, B=B)
            elapsed = time.time() - t0
            results[r] = w
            times[r]   = elapsed
            print(f"R={r:2d}  weight={w:3d}  {elapsed:.3f}s")
    else:
        wb = {r: 2 * v for r, v in ACTIVE_BOUNDS.items()} if args.pc else None

        n_workers = max(1, min(len(rounds), os.cpu_count() // 3))
        with ProcessPoolExecutor(max_workers=n_workers) as ex:
            futures = {ex.submit(run_r, (r, use_bounds, compact, wb)): r for r in rounds}
            for fut in as_completed(futures):
                r, w, elapsed = fut.result()
                results[r] = w
                times[r]   = elapsed
                print(f"R={r:2d}  weight={w:3d}  {elapsed:.3f}s")

    print()
    if args.matsui:
        print(f"{'R':>3}  {'min_weight':>10}   {'time':>8}")
        print('-' * 28)
        for r in sorted(results):
            print(f"{r:>3}  {results[r]:>10}  {times[r]:>8.3f}s")
    else:
        print(f"{'R':>3}  {'min_active':>10}  {'2*active':>8}  {'min_weight':>10}  {'gap':>4}")
        print('-' * 44)
        for r in sorted(results):
            a   = find_min_active(r, use_bounds=use_bounds, compact=compact)
            w   = results[r]
            gap = w - 2 * a
            marker = ' <--' if gap > 0 else ''
            print(f"{r:>3}  {a:>10}  {2*a:>8}  {w:>10}  {gap:>4}{marker}")


if __name__ == '__main__':
    main()
