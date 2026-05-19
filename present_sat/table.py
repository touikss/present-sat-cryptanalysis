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

    def mark_start(self, r):
        """Record the start time for round r to display a live elapsed counter.

        Args:
            r: round number.
        """
        with self._lock:
            self.start_times[r] = time.time()

    def set_testing(self, r, w):
        """Update the currently tested weight for round r (shown while solving).

        Args:
            r: round number.
            w: weight value currently being tested by the solver.
        """
        with self._lock:
            self.testing[r] = w
            if _IS_TTY:
                self._redraw_locked()

    def update(self, r, *, active=None, weight=None, trail_done=False, elapsed=None):
        """Store final results for round r and redraw the table.

        Args:
            r: round number.
            active: minimum number of active S-boxes (if computed).
            weight: minimum trail weight (if computed).
            trail_done: set to True when the trail for this round is ready.
            elapsed: total wall-clock time in seconds for this round.
        """
        with self._lock:
            if active is not None: self.active[r] = active
            if weight is not None: self.weight[r] = weight
            if elapsed is not None: self.times[r] = elapsed
            if trail_done: self.trail_done.add(r)
            self._redraw_locked()

    def _build(self):
        """Build and return the list of lines to display."""
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
                    row += [f"{gap:>4}"]
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
        """Acquire the lock and redraw the table."""
        with self._lock:
            self._redraw_locked()

    def _redraw_locked(self):
        """Redraw the table (must be called with self._lock held)."""
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


def print_trails(trail_res):
    """Print all extracted differential trails in hexadecimal.

    Args:
        trail_res: dict mapping round number to a list of R+1 difference words.
    """
    for r in sorted(trail_res):
        trail = trail_res[r]
        print(f"R={r:2d}:")
        for i, delta in enumerate(trail):
            print(f"  Δ{i} = {delta:#018x}")
        print()
