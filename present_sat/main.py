import argparse
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from .search import find_min_active, find_min_weight_fast


def run_r(r):
    """Run the min-weight search for R rounds and return (r, weight, elapsed_seconds)."""
    t0 = time.time()
    w = find_min_weight_fast(r)
    return r, w, time.time() - t0


def main():
    """CLI entry point: search min-weight differential trails up to --rmax rounds in parallel."""
    parser = argparse.ArgumentParser(description='PRESENT min-weight differential trail search')
    parser.add_argument('--rmax', type=int, default=10)
    args = parser.parse_args()

    rmax = args.rmax
    rounds = list(range(1, rmax + 1))
    n_workers = max(1, min(len(rounds), os.cpu_count() // 3))

    results = {}
    times   = {}

    with ProcessPoolExecutor(max_workers=n_workers) as ex:
        futures = {ex.submit(run_r, r): r for r in rounds}
        for fut in as_completed(futures):
            r, w, elapsed = fut.result()
            results[r] = w
            times[r]   = elapsed
            print(f"R={r:2d}  weight={w:3d}  {elapsed:.3f}s")

    print()
    print(f"{'R':>3}  {'min_active':>10}  {'2*active':>8}  {'min_weight':>10}  {'gap':>4}")
    print('-' * 44)
    for r in sorted(results):
        a   = find_min_active(r)
        w   = results[r]
        gap = w - 2 * a
        marker = ' <--' if gap > 0 else ''
        print(f"{r:>3}  {a:>10}  {2*a:>8}  {w:>10}  {gap:>4}{marker}")


if __name__ == '__main__':
    main()
