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

def _run_active(args: tuple[int, bool, str]) -> tuple[str, int, int, None, None, float]:
    r, use_bounds, solver = args
    t0 = time.time()
    a = find_min_active_sbox(r, use_bounds=use_bounds, solver=solver)
    return "active", r, a, None, None, time.time() - t0


def _run_weight(args: tuple[int, bool, dict[int, int], str]) -> tuple[str, int, None, int, None, float]:
    r, use_bounds, wb, solver = args
    t0 = time.time()
    w = find_min_trail_weight(r, use_bounds=use_bounds, weight_bounds=wb, solver=solver)
    return "weight", r, None, w, None, time.time() - t0


def _run_active_weight(args: tuple[int, bool, dict[int, int], str]) -> tuple[str, int, int, int, None, float]:
    r, use_bounds, wb, solver = args
    t0 = time.time()
    a = find_min_active_sbox(r, use_bounds=use_bounds, solver=solver)
    w = find_min_trail_weight(r, use_bounds=use_bounds, weight_bounds=wb, solver=solver)
    return "active_weight", r, a, w, None, time.time() - t0


def _run_active_trail(args: tuple[int, bool, str]) -> tuple[str, int, int, None, list[int], float]:
    r, use_bounds, solver = args
    t0 = time.time()
    a, trail = find_min_active_sbox(r, use_bounds=use_bounds, solver=solver, return_trail=True)
    return "active_trail", r, a, None, trail, time.time() - t0


def _run_weight_trail(args: tuple[int, bool, dict[int, int], str]) -> tuple[str, int, None, int, list[int], float]:
    r, use_bounds, wb, solver = args
    t0 = time.time()
    w, trail = find_min_trail_weight(r, use_bounds=use_bounds, weight_bounds=wb, solver=solver, return_trail=True)
    return "weight_trail", r, None, w, trail, time.time() - t0


def _run_active_weight_trail(args: tuple[int, bool, dict[int, int], str]) -> tuple[str, int, int, int, list[int], float]:
    r, use_bounds, wb, solver = args
    t0 = time.time()
    a = find_min_active_sbox(r, use_bounds=use_bounds, solver=solver)
    w, trail = find_min_trail_weight(r, use_bounds=use_bounds, weight_bounds=wb, solver=solver, return_trail=True)
    return "active_weight_trail", r, a, w, trail, time.time() - t0


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
# Live table
# ---------------------------------------------------------------------------

_IS_TTY = sys.stdout.isatty()


class _LiveTable:
    """Redraws itself in place using ANSI escape codes (falls back to line-by-line on non-TTY)."""

    _P = "..."  # pending placeholder

    def __init__(self, rounds: list[int], want_active: bool, want_weight: bool, want_trail: bool):
        self.rounds = rounds
        self.want_active = want_active
        self.want_weight = want_weight
        self.want_trail = want_trail
        self.active:     dict[int, int]       = {}
        self.weight:     dict[int, int]       = {}
        self.times:      dict[int, float]     = {}
        self.trail_done: set[int]             = set()
        self._drawn = 0

    def update(self, r: int, *,
               active: int | None = None,
               weight: int | None = None,
               trail_done: bool = False,
               elapsed: float | None = None) -> None:
        if active  is not None: self.active[r]  = active
        if weight  is not None: self.weight[r]  = weight
        if elapsed is not None: self.times[r]   = elapsed
        if trail_done:          self.trail_done.add(r)
        self._redraw()

    # --- rendering ----------------------------------------------------------

    def _build(self) -> list[str]:
        P = self._P
        lines: list[str] = []

        # header
        cols: list[str] = [f"{'R':>3}"]
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

        # rows
        for r in self.rounds:
            a = self.active.get(r)
            w = self.weight.get(r)
            t = self.times.get(r)

            row: list[str] = [f"{r:>3}"]
            if self.want_active:
                row += [f"{a:>10}" if a is not None else f"{P:>10}",
                        f"{2*a:>8}" if a is not None else f"{'':>8}"]
            if self.want_weight:
                row += [f"{w:>10}" if w is not None else f"{P:>10}"]
            if self.want_active and self.want_weight:
                if a is not None and w is not None:
                    gap = w - 2 * a
                    row += [f"{gap:>4}" + (" <--" if gap > 0 else "")]
                else:
                    row += [f"{'':>4}"]
            if self.want_trail:
                row += [f"{'ok':>5}" if r in self.trail_done else f"{'...':>5}"]
            row += [f"{t:>7.3f}s" if t is not None else f"{'':>8}"]

            lines.append("  ".join(row))

        return lines

    def _redraw(self) -> None:
        lines = self._build()
        if _IS_TTY:
            if self._drawn:
                sys.stdout.write(f"\033[{self._drawn}A")  # cursor up
            for line in lines:
                sys.stdout.write(f"\033[2K{line}\n")      # clear + print
            sys.stdout.flush()
            self._drawn = len(lines)
        else:
            # non-TTY: print only the last completed row
            r_done = (set(self.active) | set(self.weight) | self.trail_done)
            if r_done:
                r = max(r_done)
                row_idx = self.rounds.index(r) + 2  # +2 for header + separator
                sys.stdout.write(lines[row_idx] + "\n")
                sys.stdout.flush()


# ---------------------------------------------------------------------------
# Trail display
# ---------------------------------------------------------------------------

def _print_trails(trail_res: dict[int, list[int]]) -> None:
    for r in sorted(trail_res):
        trail = trail_res[r]
        print(f"R={r:2d}:")
        for i, delta in enumerate(trail):
            print(f"  Δ{i} = {delta:#018x}")
        print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """CLI entry point for PRESENT differential trail search."""
    parser = argparse.ArgumentParser(description="PRESENT differential trail search")
    parser.add_argument("--rmin",    type=int, default=1)
    parser.add_argument("--rmax",    type=int, default=10)
    parser.add_argument("--bounds",  action="store_true",
                        help="use precomputed active-sbox prefix bounds to prune the search")
    parser.add_argument("--active",  action="store_true",
                        help="compute the minimum number of active S-boxes per round")
    parser.add_argument("--weight",  action="store_true",
                        help="compute the minimum trail weight per round")
    parser.add_argument("--trail",   action="store_true",
                        help="extract and display an optimal differential trail per round")
    parser.add_argument("--workers", type=int, default=None,
                        help="maximum number of parallel workers (default: cpu_count // 3)")
    parser.add_argument("--solver",  choices=list(SOLVERS), default="cadical",
                        help="SAT solver to use (default: cadical)")
    args = parser.parse_args()

    if not (args.active or args.weight or args.trail):
        parser.error("at least one of --active, --weight, --trail is required")

    rounds = list(range(args.rmin, args.rmax + 1))
    default_workers = max(1, os.cpu_count() // 3)
    n_workers = max(1, min(len(rounds), args.workers or default_workers))

    wb: dict[int, int] = {r: 2 * v for r, v in ACTIVE_BOUNDS.items()}
    trail_res: dict[int, list[int]] = {}

    # Select worker and argument builder based on requested outputs.
    if args.trail and args.active and args.weight:
        worker, mk_args = _run_active_weight_trail, lambda r: (r, args.bounds, wb, args.solver)
    elif args.trail and args.weight:
        worker, mk_args = _run_weight_trail,        lambda r: (r, args.bounds, wb, args.solver)
    elif args.trail and args.active:
        worker, mk_args = _run_active_trail,        lambda r: (r, args.bounds, args.solver)
    elif args.trail:
        worker, mk_args = _run_weight_trail,        lambda r: (r, args.bounds, wb, args.solver)
    elif args.active and args.weight:
        worker, mk_args = _run_active_weight,       lambda r: (r, args.bounds, wb, args.solver)
    elif args.weight:
        worker, mk_args = _run_weight,              lambda r: (r, args.bounds, wb, args.solver)
    else:
        worker, mk_args = _run_active,              lambda r: (r, args.bounds, args.solver)

    table = _LiveTable(rounds, want_active=args.active, want_weight=args.weight, want_trail=args.trail)
    if _IS_TTY and (args.active or args.weight or args.trail):
        table._redraw()  # show empty table immediately

    with ProcessPoolExecutor(max_workers=n_workers) as ex:
        futures = {ex.submit(worker, mk_args(r)): r for r in rounds}
        for res in _collect(ex, futures):
            _, r, a, w, trail, elapsed = res
            if trail is not None:
                trail_res[r] = trail
            table.update(r, active=a, weight=w, trail_done=trail is not None, elapsed=elapsed)

    if args.trail:
        print()
        _print_trails(trail_res)


if __name__ == "__main__":
    main()
