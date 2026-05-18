import argparse
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from .search import find_min_active, find_min_weight, ACTIVE_BOUNDS


def _run_sat(args: tuple[int, bool, dict[int, int] | None]) -> tuple[int, int, float]:
    """Worker: run SAT min-weight search for R rounds, return (r, weight, elapsed)."""
    r, use_bounds, wb = args
    t0 = time.time()
    w = find_min_weight(r, use_bounds=use_bounds, weight_bounds=wb)
    return r, w, time.time() - t0


def main() -> None:
    parser = argparse.ArgumentParser(description='PRESENT min-weight differential trail search')
    parser.add_argument('--rmin',   type=int, default=1)
    parser.add_argument('--rmax',   type=int, default=10)
    parser.add_argument('--bounds', action='store_true',
                        help='use precomputed active-sbox prefix bounds to prune the search')
    parser.add_argument('--pc',     action='store_true',
                        help='add PC1/PC2 weight lower-bound constraints')
    args = parser.parse_args()

    rounds = list(range(args.rmin, args.rmax + 1))
    results: dict[int, int] = {}
    times: dict[int, float] = {}

    wb: dict[int, int] | None = {r: 2 * v for r, v in ACTIVE_BOUNDS.items()} if args.pc else None

    n_workers = max(1, min(len(rounds), os.cpu_count() // 3))
    with ProcessPoolExecutor(max_workers=n_workers) as ex:
        futures = {ex.submit(_run_sat, (r, args.bounds, wb)): r for r in rounds}
        for fut in as_completed(futures):
            r, w, elapsed = fut.result()
            results[r] = w
            times[r] = elapsed
            print(f"R={r:2d}  weight={w:3d}  {elapsed:.3f}s")

    print()
    print(f"{'R':>3}  {'min_active':>10}  {'2*active':>8}  {'min_weight':>10}  {'gap':>4}")
    print('-' * 44)
    for r in sorted(results):
        a = find_min_active(r, use_bounds=args.bounds)
        w = results[r]
        gap = w - 2 * a
        marker = ' <--' if gap > 0 else ''
        print(f"{r:>3}  {a:>10}  {2*a:>8}  {w:>10}  {gap:>4}{marker}")


if __name__ == '__main__':
    main()
