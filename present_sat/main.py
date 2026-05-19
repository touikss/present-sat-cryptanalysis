import argparse
import multiprocessing
import os
import signal
import sys
import time
import threading
from concurrent.futures import ProcessPoolExecutor, as_completed

from .search import find_min_active_sbox, find_min_trail_weight, SOLVERS


# workers run in child processes, _worker_queue is set via initializer
_worker_queue = None


def _init_worker(q):
    global _worker_queue
    _worker_queue = q


def _run_active(args):
    r, solver = args
    t0 = time.time()
    a = find_min_active_sbox(r, solver=solver)
    return "active", r, a, None, None, time.time() - t0


def _run_weight(args):
    r, solver, w_min = args
    t0 = time.time()
    w = find_min_trail_weight(r, W_min=w_min, solver=solver, progress_queue=_worker_queue)
    return "weight", r, None, w, None, time.time() - t0


def _run_active_weight(args):
    r, solver, w_min = args
    t0 = time.time()
    a = find_min_active_sbox(r, solver=solver)
    w = find_min_trail_weight(r, W_min=w_min, solver=solver, progress_queue=_worker_queue)
    return "active_weight", r, a, w, None, time.time() - t0


def _run_active_trail(args):
    r, solver = args
    t0 = time.time()
    a, trail = find_min_active_sbox(r, solver=solver, return_trail=True)
    return "active_trail", r, a, None, trail, time.time() - t0


def _run_weight_trail(args):
    r, solver, w_min = args
    t0 = time.time()
    w, trail = find_min_trail_weight(r, W_min=w_min, solver=solver, return_trail=True, progress_queue=_worker_queue)
    return "weight_trail", r, None, w, trail, time.time() - t0


def _run_active_weight_trail(args):
    r, solver, w_min = args
    t0 = time.time()
    a = find_min_active_sbox(r, solver=solver)
    w, trail = find_min_trail_weight(r, W_min=w_min, solver=solver, return_trail=True, progress_queue=_worker_queue)
    return "active_weight_trail", r, a, w, trail, time.time() - t0


def _shutdown(ex):
    print("\nInterrupted, shutting down workers...")
    procs = list(ex._processes.values()) if ex._processes else []
    ex.shutdown(wait=False, cancel_futures=True)
    for proc in procs:
        proc.terminate()
    sys.exit(1)


def _collect(ex, futures):
    signal.signal(signal.SIGTERM, lambda _sig, _frame: _shutdown(ex))
    try:
        for fut in as_completed(futures):
            yield fut.result()
    except KeyboardInterrupt:
        _shutdown(ex)


_IS_TTY = sys.stdout.isatty()


class LiveTable:
    _P = "..."

    def __init__(self, rounds, want_active, want_weight, want_trail):
        self.rounds = rounds
        self.want_active = want_active
        self.want_weight = want_weight
        self.want_trail = want_trail
        self.active = {}
        self.weight = {}
        self.testing = {}
        self.times = {}
        self.start_times = {}
        self.trail_done = set()
        self._drawn = 0
        self._lock = threading.Lock()

    def mark_start(self, r):
        with self._lock:
            self.start_times[r] = time.time()

    def set_testing(self, r, w):
        with self._lock:
            self.testing[r] = w
            if _IS_TTY:
                self._redraw_locked()

    def update(self, r, *, active=None, weight=None, trail_done=False, elapsed=None):
        with self._lock:
            if active is not None: self.active[r] = active
            if weight is not None: self.weight[r] = weight
            if elapsed is not None: self.times[r] = elapsed
            if trail_done: self.trail_done.add(r)
            self._redraw_locked()

    def _build(self):
        P = self._P
        lines = []

        cols = [f"{'R':>3}"]
        if self.want_active:
            cols += [f"{'min_active':>10}", f"{'2*active':>8}"]
        if self.want_weight:
            cols += [f"{'min_weight':>10}"]
        if self.want_active and self.want_weight:
            cols += [f"{'gap':>4}"]
        if self.want_trail:
            cols += [f"{'trail':>5}"]
        cols += [f"{'time':>8}"]

        header = "  ".join(cols)
        lines.append(header)
        lines.append("-" * len(header))

        for r in self.rounds:
            a = self.active.get(r)
            w = self.weight.get(r)
            t = self.times.get(r)

            row = [f"{r:>3}"]
            if self.want_active:
                row += [f"{a:>10}" if a is not None else f"{P:>10}",
                        f"{2*a:>8}" if a is not None else f"{'':>8}"]
            if self.want_weight:
                if w is not None:
                    row += [f"{w:>10}"]
                elif r in self.testing:
                    row += [f"{self.testing[r]:>10}"]
                else:
                    row += [f"{P:>10}"]
            if self.want_active and self.want_weight:
                if a is not None and w is not None:
                    gap = w - 2 * a
                    row += [f"{gap:>4}" + (" <--" if gap > 0 else "")]
                else:
                    row += [f"{'':>4}"]
            if self.want_trail:
                row += [f"{'ok':>5}" if r in self.trail_done else f"{'...':>5}"]
            if t is not None:
                row += [f"{t:>7.3f}s"]
            elif r in self.start_times:
                elapsed = time.time() - self.start_times[r]
                row += [f"{elapsed:>7.1f}s"]
            else:
                row += [f"{'':>8}"]

            lines.append("  ".join(row))

        return lines

    def _redraw(self):
        with self._lock:
            self._redraw_locked()

    def _redraw_locked(self):
        lines = self._build()
        if _IS_TTY:
            if self._drawn:
                sys.stdout.write(f"\033[{self._drawn}A")
            for line in lines:
                sys.stdout.write(f"\033[2K{line}\n")
            sys.stdout.flush()
            self._drawn = len(lines)
        else:
            r_done = set(self.active) | set(self.weight) | self.trail_done
            if r_done:
                r = max(r_done)
                row_idx = self.rounds.index(r) + 2
                sys.stdout.write(lines[row_idx] + "\n")
                sys.stdout.flush()


def _print_trails(trail_res):
    for r in sorted(trail_res):
        trail = trail_res[r]
        print(f"R={r:2d}:")
        for i, delta in enumerate(trail):
            print(f"  Δ{i} = {delta:#018x}")
        print()


def main():
    parser = argparse.ArgumentParser(description="PRESENT differential trail search")
    parser.add_argument("--rmin",    type=int, default=1)
    parser.add_argument("--rmax",    type=int, default=10)
    parser.add_argument("--active",  action="store_true")
    parser.add_argument("--weight",  action="store_true")
    parser.add_argument("--trail",   action="store_true")
    parser.add_argument("--seq",     action="store_true",
                        help="sequential: use weight[R-1] as lower bound for weight[R]")
    parser.add_argument("--cached",  action="store_true",
                        help="parallel: pass cached weight[R-1] as lower bound when available")
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--solver",  choices=list(SOLVERS), default="kissat")
    args = parser.parse_args()

    if not (args.active or args.weight or args.trail):
        parser.error("at least one of --active, --weight, --trail is required")

    rounds = list(range(args.rmin, args.rmax + 1))
    n_workers = max(1, min(len(rounds), args.workers or max(1, os.cpu_count() // 3)))

    trail_res = {}
    pq = multiprocessing.Queue()

    if args.trail and args.active and args.weight:
        worker, mk_args = _run_active_weight_trail, lambda r, wm=None: (r, args.solver, wm)
    elif args.trail and args.weight:
        worker, mk_args = _run_weight_trail,        lambda r, wm=None: (r, args.solver, wm)
    elif args.trail and args.active:
        worker, mk_args = _run_active_trail,        lambda r: (r, args.solver)
    elif args.trail:
        worker, mk_args = _run_weight_trail,        lambda r, wm=None: (r, args.solver, wm)
    elif args.active and args.weight:
        worker, mk_args = _run_active_weight,       lambda r, wm=None: (r, args.solver, wm)
    elif args.weight:
        worker, mk_args = _run_weight,              lambda r, wm=None: (r, args.solver, wm)
    else:
        worker, mk_args = _run_active,              lambda r: (r, args.solver)

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
        prev_weight = None
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
                wm = cache.get(r - 1)
                fut = ex.submit(worker, mk_args(r, wm))
                active_futures[fut] = r
                table.mark_start(r)

            for r in pending[:n_workers]:
                _submit(r)
            pending = pending[n_workers:]

            signal.signal(signal.SIGTERM, lambda *_: _shutdown(ex))
            try:
                while active_futures:
                    for fut in as_completed(active_futures):
                        _, r, a, w, trail, elapsed = fut.result()
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
            futures = {ex.submit(worker, mk_args(r)): r for r in rounds}
            pending_starts = list(rounds)
            for r in pending_starts[:n_workers]:
                table.mark_start(r)
            pending_starts = pending_starts[n_workers:]
            for res in _collect(ex, futures):
                _, r, a, w, trail, elapsed = res
                if trail is not None:
                    trail_res[r] = trail
                table.update(r, active=a, weight=w, trail_done=trail is not None, elapsed=elapsed)
                if pending_starts:
                    table.mark_start(pending_starts.pop(0))

    stop_timer.set()
    stop_progress.set()

    if args.trail:
        print()
        _print_trails(trail_res)


if __name__ == "__main__":
    main()
