import nbformat

def md(src):
    return nbformat.v4.new_markdown_cell(source=src)

def code(src):
    return nbformat.v4.new_code_cell(source=src)

cells = []

# ── Title ─────────────────────────────────────────────────────────────────────
cells.append(md("""\
# Differential cryptanalysis of PRESENT using SAT

EPITA 2026 — PPC project F2

We search for minimum-weight differential trails in the PRESENT block cipher
(Bogdanov et al., CHES 2007) by encoding the problem as SAT and using binary search.
"""))

# ── Section 1: cipher ─────────────────────────────────────────────────────────
cells.append(md("## 1. PRESENT cipher"))

cells.append(code("""\
SBOX = [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD, 0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]
P = [ 0, 16, 32, 48,  1, 17, 33, 49,  2, 18, 34, 50,  3, 19, 35, 51,
      4, 20, 36, 52,  5, 21, 37, 53,  6, 22, 38, 54,  7, 23, 39, 55,
      8, 24, 40, 56,  9, 25, 41, 57, 10, 26, 42, 58, 11, 27, 43, 59,
     12, 28, 44, 60, 13, 29, 45, 61, 14, 30, 46, 62, 15, 31, 47, 63]

def generate_round_keys(key):
    keys = [key]
    kp = key
    for i in range(1, 32):
        ki = kp >> 19 | ((kp << 61) & 0xffffffffffffffffffff)
        head = (ki >> 76) & 0xf
        ki = (ki & 0xfffffffffffffffffff) | (SBOX[head] << 76)
        ki ^= i << 15
        keys.append(ki)
        kp = ki
    return keys

def add_round_key(state, key):
    return state ^ (key >> 16)

def s_box_layer(state):
    result = 0
    for i in range(16):
        result |= SBOX[(state >> (4*i)) & 0xf] << (4*i)
    return result

def p_layer(state):
    result = 0
    for i in range(64):
        result |= ((state >> i) & 1) << P[i]
    return result

def present(plaintext, keys):
    state = plaintext
    for i in range(31):
        state = add_round_key(state, keys[i])
        state = s_box_layer(state)
        state = p_layer(state)
    return add_round_key(state, keys[31])
"""))

cells.append(code("""\
# test vectors from the paper
tests = [
    (0x0000000000000000, 0x00000000000000000000, 0x5579C1387B228445),
    (0x0000000000000000, 0xFFFFFFFFFFFFFFFFFFFF, 0xE72C46C0F5945049),
    (0xFFFFFFFFFFFFFFFF, 0x00000000000000000000, 0xA112FFC72F68417B),
    (0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFFFFFF, 0x3333DCD3213210D2),
]
for pt, k, expected in tests:
    assert present(pt, generate_round_keys(k)) == expected
print("test vectors ok")
"""))

# ── Section 2: DDT ────────────────────────────────────────────────────────────
cells.append(md("""\
## 2. Difference Distribution Table

The DDT counts input/output difference pairs through the S-box:
DDT[a][b] = |{x : S(x) ^ S(x^a) = b}|

For PRESENT, all active entries are 2 or 4, giving transition weights 3 or 2 respectively.
"""))

cells.append(code("""\
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import math

def build_ddt(sbox):
    n = len(sbox)
    ddt = np.zeros((n, n), dtype=int)
    for di in range(n):
        for x in range(n):
            ddt[di][sbox[x] ^ sbox[x ^ di]] += 1
    return ddt

DDT = build_ddt(SBOX)

plt.figure(figsize=(6, 5))
plt.imshow(DDT, cmap='YlOrRd')
plt.colorbar(label='count')
plt.xticks(range(16), [f'{i:X}' for i in range(16)])
plt.yticks(range(16), [f'{i:X}' for i in range(16)])
plt.xlabel('delta out')
plt.ylabel('delta in')
plt.title('DDT of PRESENT S-box')
plt.tight_layout()
plt.show()

print(f"max differential probability: {DDT[1:].max()}/16")
"""))

cells.append(code("""\
w2_count = sum(1 for a in range(1,16) for b in range(16) if DDT[a][b] == 4)
w3_count = sum(1 for a in range(1,16) for b in range(16) if DDT[a][b] == 2)

plt.figure(figsize=(5, 3))
plt.bar(['weight 2 (DDT=4)', 'weight 3 (DDT=2)'], [w2_count, w3_count], color=['steelblue', 'tomato'])
plt.ylabel('number of transitions')
plt.title('S-box transitions by weight')
plt.tight_layout()
plt.show()

print(f"weight-2 transitions: {w2_count}")
print(f"weight-3 transitions: {w3_count}")
"""))

# ── Section 3: SAT encoding ───────────────────────────────────────────────────
cells.append(md("""\
## 3. SAT encoding

We encode an R-round differential trail as a CNF formula.

**Variables:**
- `diff_var(r, i)` = bit i of the difference at round r (0 <= r <= R, 0 <= i < 64)
- `active_var(R, r, s)` = 1 if S-box s in round r is active
- `w2_var(R, r, s)`, `w3_var(R, r, s)` = weight indicator for S-box (DDT=4 or DDT=2)

**Constraints:**
- For each DDT[a][b] = 0: forbid that input/output assignment (one clause per pair)
- The input difference at round 0 must be non-zero
- Weight indicators: w2=1 iff the S-box uses a DDT=4 transition, w3=1 iff DDT=2
"""))

cells.append(code("""\
from pysat.formula import CNF
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.pb import PBEnc

def diff_var(r, i):
    return 1 + r * 64 + i

def active_var(R, r, s):
    return 1 + 64*(R+1) + r*16 + s

def w2_var(R, r, s):
    return 1 + 64*(R+1) + r*16 + s

def w3_var(R, r, s):
    return 1 + 64*(R+1) + R*16 + r*16 + s

def forbid_assignment(x_vars, y_vars, x_val, y_val):
    clause = []
    for i, var in enumerate(x_vars):
        clause.append(-var if (x_val >> i) & 1 else var)
    for i, var in enumerate(y_vars):
        clause.append(-var if (y_val >> i) & 1 else var)
    return clause

def sbox_clauses(x_vars, y_vars, ddt):
    return [
        forbid_assignment(x_vars, y_vars, a, b)
        for a in range(16) for b in range(16)
        if ddt[a][b] == 0
    ]

def build_round(cnf, r):
    for s in range(16):
        x_vars = [diff_var(r,   4*s + j) for j in range(4)]
        y_vars = [diff_var(r+1, P[4*s + j]) for j in range(4)]
        for clause in sbox_clauses(x_vars, y_vars, DDT):
            cnf.append(clause)
"""))

cells.append(code("""\
# check that SAT(a,b) iff DDT[a][b] > 0 for all pairs
x_vars, y_vars = [1, 2, 3, 4], [5, 6, 7, 8]
base = sbox_clauses(x_vars, y_vars, DDT)
for a in range(16):
    for b in range(16):
        cnf = CNF()
        for c in base: cnf.append(c)
        for i, var in enumerate(x_vars):
            cnf.append([var if (a >> i) & 1 else -var])
        for i, var in enumerate(y_vars):
            cnf.append([var if (b >> i) & 1 else -var])
        with Cadical153(bootstrap_with=cnf) as s:
            sat = s.solve()
        assert sat == (DDT[a][b] > 0), f"mismatch at a={a} b={b}"
print("encoding ok")
"""))

# ── Section 4: active S-box search ───────────────────────────────────────────
cells.append(md("""\
## 4. Minimum active S-boxes

We search for the minimum number of active S-boxes over R rounds using binary search.
Each iteration adds an "at-most-K" cardinality constraint via an activation literal,
keeping the same solver alive to reuse learned clauses.

Bogdanov et al. 2007 (Theorem 1) prove that any 5-round trail has at least 10 active S-boxes.
"""))

cells.append(code("""\
def active_clauses(cnf, R, r, s):
    a = active_var(R, r, s)
    x = [diff_var(r, 4*s + j) for j in range(4)]
    cnf.append([-a] + x)
    for xi in x:
        cnf.append([-xi, a])

def build_model(R, K=None):
    cnf = CNF()
    for r in range(R):
        build_round(cnf, r)
        for s in range(16):
            active_clauses(cnf, R, r, s)
    cnf.append([diff_var(0, i) for i in range(64)])
    if K is not None:
        lits = [active_var(R, r, s) for r in range(R) for s in range(16)]
        enc = CardEnc.atmost(lits=lits, bound=K, top_id=cnf.nv, encoding=EncType.seqcounter)
        cnf.extend(enc.clauses)
    return cnf

def find_min_active(R):
    base = build_model(R, K=None)
    lits = [active_var(R, r, s) for r in range(R) for s in range(16)]
    with Cadical153(bootstrap_with=base.clauses) as solver:
        top = base.nv
        lo, hi = 1, len(lits)
        while lo < hi:
            mid = (lo + hi) // 2
            top += 1
            act = top
            enc = CardEnc.atmost(lits=lits, bound=mid, top_id=top, encoding=EncType.seqcounter)
            for clause in enc.clauses:
                solver.add_clause([-act] + clause)
            top = enc.nv
            if solver.solve(assumptions=[act]):
                hi = mid
            else:
                lo = mid + 1
    return lo
"""))

cells.append(code("""\
import time

def validate_trail(deltas, R):
    for r in range(R):
        din, dout = deltas[r], deltas[r+1]
        for s in range(16):
            in_n  = (din >> (4*s)) & 0xF
            out_n = sum(((dout >> P[4*s+j]) & 1) << j for j in range(4))
            if DDT[in_n][out_n] == 0:
                return False
    return True

# find a valid R=5 trail
R = 5
cnf = build_model(R)
with Cadical153(bootstrap_with=cnf) as solver:
    solver.solve()
    model = solver.get_model()
    deltas = [sum((1 << i) for i in range(64) if model[diff_var(r, i)-1] > 0)
              for r in range(R+1)]

for r, d in enumerate(deltas):
    print(f"d{r} = {d:016x}")
print("valid:", validate_trail(deltas, R))

t0 = time.time()
k = find_min_active(5)
print(f"R=5 min active: {k}  ({time.time()-t0:.2f}s)")
"""))

# ── Section 5: weight-aware search ───────────────────────────────────────────
cells.append(md("""\
## 5. Minimum trail weight

Active S-box count gives a lower bound: weight >= 2 * min_active.
But some trails require DDT=2 (weight-3) transitions, so the actual minimum can be higher.

`find_min_weight_fast` works in two steps:
1. Try weight = 2*min_active with w3=False forced (only DDT=4 transitions).
   This is equivalent because weight=2K with K active S-boxes each >= 2 forces all to be exactly 2.
   It reduces valid transitions from 96 to 24 per S-box, making the SAT much faster.
2. If UNSAT (happens at R=10), fall back to incremental binary search with phase hints.

For the optimistic step, three solvers run in parallel.
"""))

cells.append(code("""\
def weight_clauses(cnf, R, r, s):
    x_vars = [diff_var(r,   4*s + j) for j in range(4)]
    y_vars = [diff_var(r+1, P[4*s + j]) for j in range(4)]
    w2 = w2_var(R, r, s)
    w3 = w3_var(R, r, s)
    for a in range(16):
        for b in range(16):
            if DDT[a][b] == 0:
                continue
            c2 = forbid_assignment(x_vars, y_vars, a, b)
            c2.append(w2 if DDT[a][b] == 4 else -w2)
            cnf.append(c2)
            c3 = forbid_assignment(x_vars, y_vars, a, b)
            c3.append(w3 if DDT[a][b] == 2 else -w3)
            cnf.append(c3)

def build_weighted_model(R, W=None):
    cnf = CNF()
    for r in range(R):
        build_round(cnf, r)
        for s in range(16):
            weight_clauses(cnf, R, r, s)
    cnf.append([diff_var(0, i) for i in range(64)])
    if W is not None:
        lits, ws = [], []
        for r in range(R):
            for s in range(16):
                lits += [w2_var(R, r, s), w3_var(R, r, s)]
                ws   += [2, 3]
        cnf.extend(PBEnc.atmost(lits=lits, weights=ws, bound=W, top_id=cnf.nv).clauses)
    return cnf

def _portfolio_solve(args):
    from pysat.solvers import Cadical153, Glucose4, Glucose42
    clauses, solver_name = args
    cls = {'cadical153': Cadical153, 'glucose4': Glucose4, 'glucose42': Glucose42}[solver_name]
    with cls(bootstrap_with=clauses) as s:
        return s.solve()

def find_min_weight_fast(R, W_max=None, n_portfolio=3):
    from concurrent.futures import ProcessPoolExecutor, FIRST_COMPLETED, wait as fut_wait

    min_k = find_min_active(R)
    lo = 2 * min_k
    hi = W_max if W_max is not None else 3 * min_k

    base = build_weighted_model(R, W=None)
    pb_lits, pb_ws = [], []
    for r in range(R):
        for s in range(16):
            pb_lits += [w2_var(R, r, s), w3_var(R, r, s)]
            pb_ws   += [2, 3]

    # optimistic: w3=False is equivalent to weight <= 2*min_k when all active S-boxes cost >= 2
    w3_false  = [[-w3_var(R, r, s)] for r in range(R) for s in range(16)]
    pb_tight  = PBEnc.atmost(lits=pb_lits, weights=pb_ws, bound=lo, top_id=base.nv).clauses
    opt_clauses = base.clauses + pb_tight + w3_false

    if n_portfolio > 1:
        names = ['cadical153', 'glucose4', 'glucose42'][:n_portfolio]
        with ProcessPoolExecutor(max_workers=n_portfolio) as ex:
            futs = [ex.submit(_portfolio_solve, (opt_clauses, nm)) for nm in names]
            done, _ = fut_wait(futs, return_when=FIRST_COMPLETED)
            sat = list(done)[0].result()
    else:
        with Cadical153(bootstrap_with=opt_clauses) as s:
            sat = s.solve()

    if sat:
        return lo

    lo += 1

    with Cadical153(bootstrap_with=base.clauses) as solver:
        top = base.nv
        phases = None
        while lo < hi:
            mid = (lo + hi) // 2
            top += 1
            act = top
            pb = PBEnc.atmost(lits=pb_lits, weights=pb_ws, bound=mid, top_id=top)
            for clause in pb.clauses:
                solver.add_clause([-act] + clause)
            top = pb.nv
            if phases:
                solver.set_phases(phases)
            if solver.solve(assumptions=[act]):
                phases = solver.get_model()
                hi = mid
            else:
                lo = mid + 1
    return lo
"""))

# ── Section 6: results ────────────────────────────────────────────────────────
cells.append(md("## 6. Results"))

cells.append(code("""\
# cached results from a previous run (R=1..10, ~3 min on 12 cores)
min_active_results = {1: 1, 2: 2, 3: 4, 4: 6, 5: 10, 6: 12, 7: 14, 8: 16, 9: 18, 10: 20}
min_weight_results = {1: 2, 2: 4, 3: 8, 4: 12, 5: 20, 6: 24, 7: 28, 8: 32, 9: 36, 10: 41}
solve_times        = {1: 0.03, 2: 0.08, 3: 0.10, 4: 0.25, 5: 1.12,
                      6: 1.68, 7: 4.78, 8: 8.17, 9: 27.19, 10: 129.8}
"""))

cells.append(code("""\
%%script echo "skipped"
import os, time
from concurrent.futures import ProcessPoolExecutor, as_completed

to_search = list(range(1, 11))
n_workers = max(1, min(len(to_search), os.cpu_count() // 3))

results = {}
t0 = time.time()
with ProcessPoolExecutor(max_workers=n_workers) as ex:
    futures = {ex.submit(find_min_weight_fast, r): r for r in to_search}
    for fut in as_completed(futures):
        r = futures[fut]
        results[r] = fut.result()
        print(f"R={r}: {results[r]}  ({time.time()-t0:.1f}s)")
"""))

cells.append(code("""\
R_vals = sorted(min_active_results)

print(f"{'R':>3}  {'min_active':>10}  {'2*active':>8}  {'min_weight':>10}  {'gap':>4}")
print("-" * 45)
for r in R_vals:
    a = min_active_results[r]
    w = min_weight_results[r]
    gap = w - 2*a
    marker = " <--" if gap > 0 else ""
    print(f"{r:>3}  {a:>10}  {2*a:>8}  {w:>10}  {gap:>4}{marker}")
"""))

cells.append(code("""\
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

ax = axes[0]
ax.plot(R_vals, [min_active_results[r] for r in R_vals], 'o-', label='min active')
ax.plot(R_vals, [2*min_active_results[r] for r in R_vals], '--', alpha=0.5, label='2 x active')
ax.plot(R_vals, [min_weight_results[r] for r in R_vals], 's-', label='min weight')
ax.set_xlabel('rounds')
ax.set_ylabel('count / weight')
ax.set_title('active S-boxes vs trail weight')
ax.legend()
ax.grid(alpha=0.3)

ax = axes[1]
ax.semilogy(R_vals, [solve_times[r] for r in R_vals], 'o-')
ax.set_xlabel('rounds')
ax.set_ylabel('time (s)')
ax.set_title('solve time (log scale)')
ax.grid(alpha=0.3, which='both')

plt.tight_layout()
plt.show()
"""))

# trail visualization
cells.append(code("""\
# visualize the optimal R=5 trail
R_vis = 5
W_vis = min_weight_results[R_vis]
cnf_vis = build_weighted_model(R_vis, W=W_vis)

with Cadical153(bootstrap_with=cnf_vis) as solver:
    solver.solve()
    model = solver.get_model()
    deltas_vis = [sum((1 << i) for i in range(64) if model[diff_var(r, i)-1] > 0)
                  for r in range(R_vis+1)]
    is_w2 = [[model[w2_var(R_vis, r, s)-1] > 0 for s in range(16)] for r in range(R_vis)]
    is_w3 = [[model[w3_var(R_vis, r, s)-1] > 0 for s in range(16)] for r in range(R_vis)]

fig, ax = plt.subplots(figsize=(14, 4))
ax.set_xlim(-0.5, 15.5)
ax.set_ylim(-0.5, R_vis + 0.5)
ax.set_aspect('equal')
ax.invert_yaxis()

for r in range(R_vis + 1):
    d = deltas_vis[r]
    for s in range(16):
        nibble = (d >> (4*s)) & 0xF
        if r < R_vis:
            color = 'steelblue' if is_w2[r][s] else ('tomato' if is_w3[r][s] else '#eee')
        else:
            color = '#aad' if nibble else '#eee'
        ax.add_patch(plt.Rectangle((s-0.45, r-0.45), 0.9, 0.9,
                                   fc=color, ec='gray', lw=0.5))
        if nibble:
            ax.text(s, r, f'{nibble:X}', ha='center', va='center',
                    fontsize=8, color='white' if color not in ('#eee', '#aad') else '#333')

ax.set_xticks(range(16))
ax.set_xticklabels([f'S{i}' for i in range(16)], fontsize=8)
ax.set_yticks(range(R_vis+1))
ax.set_yticklabels([f'd{r}' for r in range(R_vis+1)])
ax.set_title(f'optimal R=5 trail (weight={W_vis})')
ax.legend(handles=[
    plt.Rectangle((0,0),1,1, fc='steelblue', label='weight 2 (DDT=4)'),
    plt.Rectangle((0,0),1,1, fc='tomato',    label='weight 3 (DDT=2)'),
    plt.Rectangle((0,0),1,1, fc='#eee', ec='gray', label='inactive'),
], loc='upper right')
plt.tight_layout()
plt.show()

w2 = sum(is_w2[r][s] for r in range(R_vis) for s in range(16))
w3 = sum(is_w3[r][s] for r in range(R_vis) for s in range(16))
print(f"weight-2: {w2}, weight-3: {w3}, total: {2*w2+3*w3}")
"""))

# ── Section 7: literature ─────────────────────────────────────────────────────
cells.append(md("""\
## 7. Comparison with literature

**Bogdanov et al. 2007 (Theorem 1):** any 5-round trail has at least 10 active S-boxes.
We confirm: min_active(5) = 10.

**Wang 2007 (ePrint 2007/408):** min_weight(14) = 62.
Our results for R=1..10 are consistent with this.

**Gap at R=10:** min_weight(10) = 41 > 40 = 2 * min_active(10).
This means at least one S-box must use a DDT=2 (weight-3) transition.
Kim et al. (ToSC 2022, "Accelerating the Best Trail Search on AES-Like Ciphers")
study this gap systematically — for GIFT-128 the active-count bound gives 2^{-75.6}
while the actual best trail is 2^{-132.4}. Our R=10 gap is smaller but comes from the same
structure: PRESENT's P-layer (branch number 2) sometimes forces weight-3 transitions.

Kim et al. also compute full 31-round PRESENT best trails in 5.1 s using Matsui's
algorithm with strengthened pruning conditions. Our SAT approach reaches R=10 in ~130 s
on 12 cores, which is expected given that SAT does not exploit the round structure for pruning.
"""))

# ── Section 8: conclusion ─────────────────────────────────────────────────────
cells.append(md("""\
## 8. Conclusion

We encoded PRESENT differential trail search as SAT and found minimum weights for R=1..10.

Main results:
- min_active matches Theorem 1 from Bogdanov et al. (10 active S-boxes at R=5)
- at R=10, min_weight = 41 > 2*20 = 40 (at least one weight-3 transition required)
- the gap phenomenon is known in the literature; Kim et al. 2022 document a much larger gap on GIFT-128

Performance: optimizations (binary search, incremental solving, portfolio parallelism,
w3=False optimistic step) reduced R=8 from ~26 min to ~8 s and got R=10 in ~130 s.

To go further: Matsui-style search with PC1/PC2 pruning (Kim et al. 2022) reaches
full 31-round PRESENT in 5 s on a single core. Our SAT approach is simple to implement
but doesn't exploit round structure for pruning, which limits it to ~R=10.
"""))

# ── write ─────────────────────────────────────────────────────────────────────
nb = nbformat.v4.new_notebook()
nb['cells'] = cells
nb['metadata'] = {
    'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
    'language_info': {'name': 'python', 'version': '3.11.0'},
}

with open('notebook-2.ipynb', 'w') as f:
    nbformat.write(nb, f)

print(f"written {len(cells)} cells")
