"""Plot minimum trail weight and solve times from benchmark.json.

Usage: python scripts/plot_benchmark.py [benchmark.json] [output.png]
"""

import json
import pathlib
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
SERIES = [
    ("min_weight_kissat_seq", "kissat-seq (lower bound = w[R-1] + 2)", "tab:orange"),
    ("min_weight_kissat", "kissat", "tab:green"),
    ("min_weight_cadical", "cadical", "tab:blue"),
]


def main():
    src = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "benchmark.json"
    dst = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "images" / "benchmark.png"
    data = json.loads(src.read_text())

    fig, (ax_w, ax_t) = plt.subplots(1, 2, figsize=(12, 4.5))

    seq = data["min_weight_kissat_seq"]
    rounds = sorted(map(int, seq))
    ax_w.plot(rounds, [seq[str(r)]["min_weight"] for r in rounds], "o-", color="tab:orange")
    ax_w.axhline(64, color="red", linestyle="--", linewidth=1, label="w = 64 (security threshold)")
    ax_w.set_xlabel("Rounds R")
    ax_w.set_ylabel("Minimum differential trail weight")
    ax_w.set_title("PRESENT: minimum trail weight")
    ax_w.grid(alpha=0.3)
    ax_w.legend()

    for key, label, color in SERIES:
        if key not in data:
            continue
        rs = sorted(map(int, data[key]))
        ax_t.plot(rs, [data[key][str(r)]["time"] for r in rs], "o-", color=color, label=label, markersize=4)
    ax_t.set_yscale("log")
    ax_t.set_xlabel("Rounds R")
    ax_t.set_ylabel("Solve time (s, log scale)")
    ax_t.set_title("Time to find the minimum weight")
    ax_t.grid(alpha=0.3, which="both")
    ax_t.legend()

    fig.tight_layout()
    fig.savefig(dst, dpi=130)
    print(f"wrote {dst}")


if __name__ == "__main__":
    main()
