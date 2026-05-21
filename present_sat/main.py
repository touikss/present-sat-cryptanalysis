import argparse
import json
import multiprocessing
import os
import pathlib
import signal
import sys
import time
import threading
from concurrent.futures import ProcessPoolExecutor, as_completed

from .search import find_min_active_sbox, find_min_trail_weight, SOLVERS, WEIGHT_BOUNDS
from .display import LiveTable, print_trails, print_benchmark, _IS_TTY

_DEFAULT_BENCHMARK = pathlib.Path(__file__).parent.parent / "benchmark.json"


# workers run in child processes, _worker_queue is set via initializer
_worker_queue = None


def _init_worker(q):
    """Initialize the global progress queue in each worker process.

    Args:
        q: multiprocessing.Queue used to send (round, W) progress updates.
    """
    global _worker_queue
    _worker_queue = q


def _run_worker(args):
    """Worker: compute requested quantities for one round.

    Args:
        args: tuple (r, solver, w_min, do_active, do_weight, do_trail).
    """
    r, solver, w_min, do_active, do_weight, do_trail = args
    t0 = time.time()
    a = w = trail = None
    if do_active:
        if do_trail and not do_weight:
            a, trail = find_min_active_sbox(r, solver=solver, return_trail=True)
        else:
            a = find_min_active_sbox(r, solver=solver)
    if do_weight:
        ret = find_min_trail_weight(r, W_min=w_min, solver=solver,
                                    return_trail=do_trail, progress_queue=_worker_queue)
        if do_trail:
            w, trail = ret
        else:
            w = ret
    return r, a, w, trail, time.time() - t0


def _shutdown(ex):
    """Terminate all worker processes and exit on interrupt.

    Args:
        ex: the ProcessPoolExecutor to shut down.
    """
    print("\nInterrupted, shutting down workers...")
    procs = list(ex._processes.values()) if ex._processes else []
    ex.shutdown(wait=False, cancel_futures=True)
    for proc in procs:
        proc.terminate()
    sys.exit(1)


def _collect(ex, futures):
    """Yield results from futures, handling SIGTERM and KeyboardInterrupt.

    Args:
        ex: the ProcessPoolExecutor (used for clean shutdown on interrupt).
        futures: dict mapping Future to round number.
    """
    signal.signal(signal.SIGTERM, lambda _sig, _frame: _shutdown(ex))
    try:
        for fut in as_completed(futures):
            yield fut.result()
    except KeyboardInterrupt:
        _shutdown(ex)


def main():
    parser = argparse.ArgumentParser(description="PRESENT differential trail search")
    parser.add_argument("--rmin", type=int, default=1, help="first round to compute (default: 1)")
    parser.add_argument("--rmax", type=int, default=10, help="last round to compute (default: 10)")
    parser.add_argument("--active", action="store_true", help="find the minimum number of active S-boxes per round")
    parser.add_argument("--weight", action="store_true", help="find the minimum differential trail weight per round")
    parser.add_argument("--trail", action="store_true", help="recover and print an optimal differential trail per round")
    parser.add_argument("--seq", action="store_true", help="sequential mode: use weight[R-1] as lower bound for weight[R] (only 1 worker used)")
    parser.add_argument("--cached", action="store_true", help="parallel mode: use cached weight[R-1] as lower bound for weight[R] (multiple workers used)")
    parser.add_argument("--workers", type=int, default=None, help="number of parallel worker processes (default: cpu_count / 3)")
    parser.add_argument("--solver", choices=list(SOLVERS), default="kissat", help="SAT solver backend (default: kissat)")
    parser.add_argument("--benchmark", metavar="FILE", nargs="?", const=str(_DEFAULT_BENCHMARK), help="display saved benchmark results (default: benchmark.json)")
    args = parser.parse_args()

    if args.benchmark is not None:
        path = pathlib.Path(args.benchmark)
        if not path.exists():
            parser.error(f"benchmark file not found: {path}")
        with open(path) as f:
            data = json.load(f)
        print_benchmark(data)
        return

    if not (args.active or args.weight or args.trail):
        parser.error("at least one of --active, --weight, --trail is required")

    rounds = list(range(args.rmin, args.rmax + 1))
    n_workers = max(1, min(len(rounds), args.workers or max(1, os.cpu_count() // 3)))

    trail_res = {}
    pq = multiprocessing.Queue()

    do_weight = args.weight or (args.trail and not args.active)
    mk_args = lambda r, wm=None: (r, args.solver, wm, args.active, do_weight, args.trail)

    opts = []
    if args.seq:    opts.append("seq")
    if args.cached: opts.append("cached")
    print(f"solver: {args.solver}" + (f"  opts: {', '.join(opts)}" if opts else ""))

    table = LiveTable(rounds, want_active=args.active, want_weight=args.weight, want_trail=args.trail)
    if _IS_TTY:
        table._redraw()

    stop_timer = threading.Event()
    if _IS_TTY:
        def _timer():
            while not stop_timer.wait(1.0):
                table._redraw()
        threading.Thread(target=_timer, daemon=True).start()

    stop_progress = threading.Event()
    def _progress_reader():
        while not stop_progress.is_set():
            try:
                r, w = pq.get(timeout=0.1)
                table.set_testing(r, w)
            except Exception:
                pass
    threading.Thread(target=_progress_reader, daemon=True).start()

    if args.seq and (args.weight or args.trail):
        prev_weight = WEIGHT_BOUNDS.get(rounds[0] - 1)
        for r in rounds:
            table.mark_start(r)
            t0 = time.time()
            a_val = find_min_active_sbox(r, solver=args.solver) if args.active else None
            ret = find_min_trail_weight(r, W_min=prev_weight, solver=args.solver,
                                        return_trail=args.trail, progress_queue=pq)
            if args.trail:
                w_val, trail = ret
                trail_res[r] = trail
            else:
                w_val = ret
            prev_weight = w_val
            table.update(r, active=a_val, weight=w_val,
                         trail_done=r in trail_res, elapsed=time.time() - t0)

    elif args.cached and (args.weight or args.trail):
        cache = {}
        pending = list(rounds)
        with ProcessPoolExecutor(max_workers=n_workers, initializer=_init_worker, initargs=(pq,)) as ex:
            active_futures = {}

            def _submit(r):
                wm = cache.get(r - 1, WEIGHT_BOUNDS.get(r - 1))
                fut = ex.submit(_run_worker, mk_args(r, wm))
                active_futures[fut] = r
                table.mark_start(r)

            for r in pending[:n_workers]:
                _submit(r)
            pending = pending[n_workers:]

            signal.signal(signal.SIGTERM, lambda *_: _shutdown(ex))
            try:
                while active_futures:
                    for fut in as_completed(active_futures):
                        r, a, w, trail, elapsed = fut.result()
                        del active_futures[fut]
                        if w is not None:
                            cache[r] = w
                        if trail is not None:
                            trail_res[r] = trail
                        table.update(r, active=a, weight=w,
                                     trail_done=trail is not None, elapsed=elapsed)
                        if pending:
                            _submit(pending.pop(0))
                        break
            except KeyboardInterrupt:
                _shutdown(ex)

    else:
        with ProcessPoolExecutor(max_workers=n_workers, initializer=_init_worker, initargs=(pq,)) as ex:
            futures = {ex.submit(_run_worker, mk_args(r)): r for r in rounds}
            pending_starts = list(rounds)
            for r in pending_starts[:n_workers]:
                table.mark_start(r)
            pending_starts = pending_starts[n_workers:]
            for res in _collect(ex, futures):
                r, a, w, trail, elapsed = res
                if trail is not None:
                    trail_res[r] = trail
                table.update(r, active=a, weight=w, trail_done=trail is not None, elapsed=elapsed)
                if pending_starts:
                    table.mark_start(pending_starts.pop(0))

    stop_timer.set()
    stop_progress.set()

    if args.trail:
        print()
        print_trails(trail_res)


if __name__ == "__main__":
    main()
