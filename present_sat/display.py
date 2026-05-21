import sys
import threading
import time

_IS_TTY = sys.stdout.isatty()


class LiveTable:
    """Terminal table that redraws itself in place using ANSI escape codes.

    Falls back to printing one line per completed round on non-TTY outputs.

    Args:
        rounds: ordered list of round numbers to display.
        want_active: whether to show the min active S-box column.
        want_weight: whether to show the min weight column.
        want_trail: whether to show the trail status column.
    """

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
        self._printed_rows = set()
        self._header_printed = False

    def mark_start(self, r):
        with self._lock:
            self.start_times[r] = time.time()

    def set_testing(self, r, w):
        with self._lock:
            self.testing[r] = w

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
                    row += [f"{w - 2*a:>4}"]
                else:
                    row += [f"{'':>4}"]
            if self.want_trail:
                row += [f"{'ok':>5}" if r in self.trail_done else f"{'...':>5}"]
            if t is not None:
                row += [f"{t:>7.3f}s"]
            elif r in self.start_times:
                row += [f"{time.time() - self.start_times[r]:>7.1f}s"]
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
            if not self._header_printed:
                sys.stdout.write(lines[0] + "\n")
                sys.stdout.write(lines[1] + "\n")
                sys.stdout.flush()
                self._header_printed = True
            for r in self.rounds:
                if r not in self._printed_rows and self.times.get(r) is not None:
                    row_idx = self.rounds.index(r) + 2
                    sys.stdout.write(lines[row_idx] + "\n")
                    sys.stdout.flush()
                    self._printed_rows.add(r)


def print_benchmark(data: dict):
    """Display benchmark.json data as formatted tables.

    Args:
        data: parsed benchmark.json dict.
    """
    active_solvers = [k for k in ("min_active_kissat", "min_active_cadical") if k in data]
    if active_solvers:
        print("Min active S-boxes")
        solvers_short = [k.replace("min_active_", "") for k in active_solvers]
        header_parts = [f"{'R':>3}"]
        for s in solvers_short:
            header_parts += [f"{'min_active':>12}", f"{'time(s)':>9}"]
        separator_parts = [f"{'solver':>3}"]
        for s in solvers_short:
            separator_parts += [f"{s:>12}", f"{'':>9}"]
        header = "  ".join(header_parts)
        solver_row = "  ".join(separator_parts)
        print(solver_row)
        print(header)
        print("-" * len(header))
        all_rounds = sorted(
            {int(r) for k in active_solvers for r in data[k]}, key=int
        )
        for r in all_rounds:
            row = [f"{r:>3}"]
            for k in active_solvers:
                entry = data[k].get(str(r))
                if entry:
                    row += [f"{entry['min_active']:>12}", f"{entry['time']:>9.3f}"]
                else:
                    row += [f"{'—':>12}", f"{'—':>9}"]
            print("  ".join(row))
        print()

    weight_solvers = [
        ("min_weight_kissat_seq", "kissat-seq"),
        ("min_weight_kissat",      "kissat"),
        ("min_weight_cadical",     "cadical"),
    ]
    weight_solvers = [(k, label) for k, label in weight_solvers if k in data]
    if weight_solvers:
        print("Min trail weight")
        header_parts = [f"{'R':>3}"]
        for _, label in weight_solvers:
            header_parts += [f"{'min_weight':>12}", f"{'time(s)':>10}"]
        solver_parts = [f"{'solver':>3}"]
        for _, label in weight_solvers:
            solver_parts += [f"{label:>12}", f"{'':>10}"]
        header = "  ".join(header_parts)
        solver_row = "  ".join(solver_parts)
        print(solver_row)
        print(header)
        print("-" * len(header))
        all_rounds = sorted(
            {int(r) for k, _ in weight_solvers for r in data[k]}, key=int
        )
        for r in all_rounds:
            row = [f"{r:>3}"]
            for k, _ in weight_solvers:
                entry = data[k].get(str(r))
                if entry:
                    row += [f"{entry['min_weight']:>12}", f"{entry['time']:>10.3f}"]
                else:
                    row += [f"{'—':>12}", f"{'—':>10}"]
            print("  ".join(row))
        print()


def print_trails(trail_res):
    for r in sorted(trail_res):
        trail = trail_res[r]
        print(f"R={r:2d}:")
        for i, delta in enumerate(trail):
            print(f"  Δ{i} = {delta:#018x}")
        print()
