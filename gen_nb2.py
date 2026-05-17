import nbformat

def md(src):
    return nbformat.v4.new_markdown_cell(source=src)

def code(src):
    return nbformat.v4.new_code_cell(source=src)

cells = []

# ── Title ─────────────────────────────────────────────────────────────────────
cells.append(md("""\
# Cryptanalyse différentielle de PRESENT par SAT

EPITA 2026 — Programmation par Contraintes — Projet F2

La cryptanalyse différentielle (Biham & Shamir, 1990) consiste à étudier comment une différence
$\\Delta_{in}$ entre deux textes clairs se propage à travers les tours d'un chiffrement. Si on
trouve un chemin différentiel $\\Delta_0 \\to \\Delta_1 \\to \\cdots \\to \\Delta_R$ de haute
probabilité, on peut monter une attaque à clé connue pour récupérer des bits de clé du dernier tour.

La probabilité d'un chemin est le produit des probabilités de chaque transition S-box active :
$$\\text{prob} = \\prod_i \\frac{\\text{DDT}[a_i][b_i]}{16}$$
On la représente en $-\\log_2$ : **poids** $w = -\\log_2(\\text{prob})$.
Trouver le **chemin de poids minimum** revient à trouver la meilleure attaque différentielle possible.

Ici on encode ce problème en SAT et on utilise une recherche binaire incrémentale pour trouver
le poids minimum sur R=1..10 tours de PRESENT (Bogdanov et al., CHES 2007).
"""))

# ── imports ───────────────────────────────────────────────────────────────────
cells.append(code("""\
import sys
sys.path.insert(0, '.')

from present_sat.present import SBOX, P, DDT, encrypt, generate_round_keys, build_ddt, validate_trail
from present_sat.encoding import (
    diff_var, active_var, w2_var, w3_var,
    sbox_clauses, build_round, build_model, build_weighted_model,
)
from present_sat.search import find_min_active, find_min_weight_fast
"""))

# ── 1. PRESENT ────────────────────────────────────────────────────────────────
cells.append(md("""\
## 1. PRESENT

PRESENT est un chiffrement par blocs ultra-léger (Bogdanov et al., CHES 2007) : 64 bits, clé 80 bits,
31 tours identiques. Sa structure SPN (Substitution-Permutation Network) le rend particulièrement
adapté à l'analyse différentielle car chaque tour est indépendant et la propagation des différences
ne dépend pas de la clé (les $\\oplus$ de clé disparaissent dans le calcul de différences).

Chaque tour :
1. **AddRoundKey** — $\\oplus$ avec les 64 bits de sous-clé
2. **SboxLayer** — 16 S-boxes $4 \\to 4$ bits en parallèle
3. **PLayer** — permutation bit fixe (même pour tous les tours)
"""))


cells.append(code("""\
tests = [
    (0x0000000000000000, 0x00000000000000000000, 0x5579C1387B228445),
    (0x0000000000000000, 0xFFFFFFFFFFFFFFFFFFFF, 0xE72C46C0F5945049),
    (0xFFFFFFFFFFFFFFFF, 0x00000000000000000000, 0xA112FFC72F68417B),
    (0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFFFFFF, 0x3333DCD3213210D2),
]
for pt, k, expected in tests:
    assert encrypt(pt, generate_round_keys(k)) == expected
print("test vectors ok")
"""))

# ── 2. DDT ────────────────────────────────────────────────────────────────────
cells.append(md("""\
## 2. Table de Distribution des Différences (DDT)

La DDT caractérise complètement le comportement différentiel d'une S-box :

$$\\text{DDT}[a][b] = \\left|\\{ x \\in \\{0,\\ldots,15\\} : S(x) \\oplus S(x \\oplus a) = b \\}\\right|$$

La probabilité de la transition $a \\to b$ est $\\text{DDT}[a][b]/16$. Pour qu'une S-box soit
active dans un chemin différentiel, il faut $a \\neq 0$ et $\\text{DDT}[a][b] > 0$.

Pour PRESENT, toutes les entrées actives valent 2 ou 4 (pas de valeurs intermédiaires).
Cela simplifie l'encodage SAT : chaque transition active a exactement un poids entier.
- $\\text{DDT}=4 \\Rightarrow \\text{prob} = 4/16 = 2^{-2} \\Rightarrow$ **poids 2**
- $\\text{DDT}=2 \\Rightarrow \\text{prob} = 2/16 = 2^{-3} \\Rightarrow$ **poids 3**

La probabilité différentielle maximale (MDP) vaut $4/16 = 2^{-2}$, ce qui est relativement élevé
mais compensé par le nombre de S-boxes actives qui croît avec le nombre de tours.
"""))

cells.append(code("""\
import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(6, 5))
plt.imshow(DDT, cmap='YlOrRd')
plt.colorbar(label='count')
plt.xticks(range(16), [f'{i:X}' for i in range(16)])
plt.yticks(range(16), [f'{i:X}' for i in range(16)])
plt.xlabel('$\\\\Delta$ out')
plt.ylabel('$\\\\Delta$ in')
plt.title('DDT — S-box PRESENT')
plt.tight_layout()
plt.show()

print(f"probabilité différentielle max : {DDT[1:].max()}/16")
"""))

cells.append(code("""\
w2_count = sum(1 for a in range(1, 16) for b in range(16) if DDT[a][b] == 4)
w3_count = sum(1 for a in range(1, 16) for b in range(16) if DDT[a][b] == 2)

plt.figure(figsize=(5, 3))
plt.bar(['poids 2 (DDT=4)', 'poids 3 (DDT=2)'], [w2_count, w3_count],
        color=['steelblue', 'tomato'])
plt.ylabel('nombre de transitions')
plt.title('Transitions S-box par poids')
plt.tight_layout()
plt.show()

print(f"transitions poids 2 : {w2_count}")
print(f"transitions poids 3 : {w3_count}")
"""))

# ── 3. Encodage SAT ───────────────────────────────────────────────────────────
cells.append(md("""\
## 3. Encodage SAT

Un chemin différentiel sur $R$ tours est un tuple $( \\Delta_0, \\Delta_1, \\ldots, \\Delta_R )$ où :
- chaque $\\Delta_r$ est un vecteur de 64 bits représentant la différence en entrée du tour $r$
- pour chaque S-box $s$, l'entrée $a$ (nibble $s$ de $\\Delta_r$) et la sortie $b$ (nibble $s$
  de $\\Delta_{r+1}$ après P-layer) doivent satisfaire $\\text{DDT}[a][b] > 0$

**Idée** : encoder chaque contrainte $\\text{DDT}[a][b]=0$ comme une clause SAT qui interdit
l'affectation (entrée$=a$, sortie$=b$). Un solveur SAT trouve un chemin valide ou prouve qu'il n'en existe pas.

**Variables** (entiers positifs = littéraux PySAT) :
- `diff_var(r, i)` — bit $i$ de la différence $\\Delta_r$ (64 bits par tour, $R+1$ couches)
- `active_var(R, r, s)` — vaut 1 si la S-box $s$ du tour $r$ est active (entrée $\\neq 0$)
- `w2_var(R, r, s)`, `w3_var(R, r, s)` — indicateurs de poids ($\\text{DDT}=4$ ou $\\text{DDT}=2$)

**Contraintes** : pour chaque paire $(a, b)$ avec $\\text{DDT}[a][b]=0$, on interdit l'affectation
correspondante (une clause par paire invalide). Le nombre de clauses par S-box est
$256 - |\\{(a,b) : \\text{DDT}[a][b] > 0\\}| \\approx 160$.
"""))

cells.append(code("""\
from pysat.formula import CNF
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.pb import PBEnc
"""))

cells.append(code("""\
x_vars, y_vars = [1, 2, 3, 4], [5, 6, 7, 8]
base_clauses = sbox_clauses(x_vars, y_vars, DDT)

for a in range(16):
    for b in range(16):
        cnf = CNF()
        for c in base_clauses:
            cnf.append(c)
        for i, var in enumerate(x_vars):
            cnf.append([var if (a >> i) & 1 else -var])
        for i, var in enumerate(y_vars):
            cnf.append([var if (b >> i) & 1 else -var])
        with Cadical153(bootstrap_with=cnf) as solver:
            sat = solver.solve()
        assert sat == (DDT[a][b] > 0), f"erreur a={a} b={b}"
print("encodage ok")
"""))

# ── 4. Minimum de S-boxes actives ─────────────────────────────────────────────
cells.append(md("""\
## 4. Nombre minimum de S-boxes actives

Le nombre de S-boxes actives donne une borne inférieure sur le poids : chaque S-box active
contribue au moins 2 ($\\text{DDT} \\leq 4 < 16$, donc $\\text{prob} \\leq 2^{-2}$).
Donc $\\text{poids} \\geq 2 \\times \\text{min\\_active}$.

On cherche le plus petit $K$ tel qu'il existe un chemin valide à exactement $K$ S-boxes actives.
C'est un problème d'optimisation que l'on résout par **recherche binaire** sur $K$.

**Solver incrémental** : plutôt que de reconstruire un nouveau problème SAT pour chaque $K$,
on garde le même solver (CaDiCaL) actif entre les itérations. Les solveurs CDCL accumulent
des clauses apprises (lemmes) qui élaguent les branches futures — les relancer depuis zéro
ferait perdre tout ce travail. La contrainte « au plus $K$ actives » est ajoutée via un
**littéral d'hypothèse** (assumption) : on peut la désactiver à l'itération suivante sans
modifier la base de clauses du solver.

Bogdanov et al. (Theorem 1) : tout chemin sur 5 tours a au moins 10 S-boxes actives.
"""))


cells.append(code("""\
import time

R = 5
cnf = build_model(R)
with Cadical153(bootstrap_with=cnf) as solver:
    solver.solve()
    model = solver.get_model()
    deltas = [
        sum((1 << i) for i in range(64) if model[diff_var(r, i) - 1] > 0)
        for r in range(R + 1)
    ]

for r, d in enumerate(deltas):
    print(f"d{r} = {d:016x}")
print("valide :", validate_trail(deltas, R))

t0 = time.time()
k = find_min_active(5)
print(f"R=5 min actives : {k}  ({time.time()-t0:.2f}s)")
"""))

# ── 5. Poids minimum des chemins ─────────────────────────────────────────────
cells.append(md("""\
## 5. Poids minimum des chemins différentiels

Le poids d'un chemin est la somme des poids de chaque S-box active : 2 si $\\text{DDT}=4$,
3 si $\\text{DDT}=2$. La section 4 donne la borne inférieure $2 \\cdot \\text{min\\_active}$,
mais le vrai minimum peut être plus élevé si aucun chemin de poids $2K$ n'existe
(certaines transitions $\\text{DDT}=2$ sont alors forcées).

**Algorithme en deux phases :**

1. **Étape optimiste** — on force toutes les variables `w3` à False (interdire $\\text{DDT}=2$)
   et on cherche un chemin de poids $\\leq 2K$. Cette contrainte est *équivalente* (pas restrictive) :
   si un chemin de poids $\\leq 2K$ existe avec $K$ actives de poids $\\geq 2$, chacune pèse
   exactement 2, donc `w3=False`. L'intérêt est algorithmique : on passe de 96 transitions valides
   à 24 par S-box, réduisant l'espace d'un facteur $\\sim 4$ et accélérant la propagation unitaire.

2. **Fallback binaire** — si l'étape optimiste est UNSAT ($\\text{min\\_weight} > 2K$), on fait une
   recherche binaire sur le poids avec le même solver incrémental. À chaque itération SAT,
   le modèle trouvé sert de **warm-start de phase** pour la suivante (`set_phases`), ce qui
   guide le solver vers les solutions légères en premier.

**Portfolio** : l'étape optimiste lance CaDiCaL, Glucose4 et Glucose42 en parallèle sur des
processus séparés (`ProcessPoolExecutor`). On retourne dès que le premier répond — les solveurs
CDCL ont des comportements très différents selon la structure du problème, donc le meilleur
varie d'un $R$ à l'autre.
"""))



# ── 6. Résultats SAT R=1..10 ─────────────────────────────────────────────────
cells.append(md("""\
## 6. Résultats SAT — R = 1 à 10

Résultats mis en cache (temps total $\\sim 3$ min sur 12 cœurs, calcul parallèle $R=1..10$ simultanément).
La cellule de calcul est désactivée (`%%script echo "skipped"`) pour ne pas relancer à chaque exécution.
"""))

cells.append(code("""\
min_active_results = {1: 1, 2: 2, 3: 4, 4: 6, 5: 10, 6: 12, 7: 14, 8: 16, 9: 18, 10: 20}
min_weight_results = {1: 2, 2: 4, 3: 8, 4: 12, 5: 20, 6: 24, 7: 28, 8: 32, 9: 36, 10: 41}
solve_times        = {1: 0.03, 2: 0.08, 3: 0.10, 4: 0.25, 5: 1.12,
                      6: 1.68, 7: 4.78, 8: 8.17, 9: 27.19, 10: 129.8}
"""))

cells.append(code("""\
%%script echo "skipped"
import os
from concurrent.futures import ProcessPoolExecutor, as_completed

to_search = list(range(1, 11))
n_workers = max(1, min(len(to_search), os.cpu_count() // 3))

computed = {}
t0 = time.time()
with ProcessPoolExecutor(max_workers=n_workers) as ex:
    futures = {ex.submit(find_min_weight_fast, r): r for r in to_search}
    for fut in as_completed(futures):
        r = futures[fut]
        computed[r] = fut.result()
        print(f"R={r}: {computed[r]}  ({time.time()-t0:.1f}s total)")
"""))

cells.append(code("""\
R_vals = sorted(min_active_results)

print(f"{'R':>3}  {'min_actives':>11}  {'2×actif':>7}  {'min_poids':>9}  {'gap':>4}")
print("-" * 42)
for r in R_vals:
    a   = min_active_results[r]
    w   = min_weight_results[r]
    gap = w - 2 * a
    marker = " <--" if gap > 0 else ""
    print(f"{r:>3}  {a:>11}  {2*a:>7}  {w:>9}  {gap:>4}{marker}")
"""))

cells.append(md("""\
**Lecture des résultats :**

Pour $R=1..9$, $\\text{min\\_weight} = 2 \\times \\text{min\\_active}$ : tous les chemins optimaux
n'utilisent que des transitions $\\text{DDT}=4$ (poids 2). La borne inférieure est atteinte.

À **R=10**, le gap apparaît : $\\text{min\\_weight} = 41 > 40 = 2 \\times 20$. Cela signifie
qu'aucun chemin valide de poids 40 n'existe — tout chemin optimal sur 10 tours est forcé
d'avoir au moins une transition $\\text{DDT}=2$ (poids 3). C'est une propriété structurelle
de PRESENT confirmée par le SAT.

En termes de sécurité : la meilleure attaque différentielle sur 10 tours a probabilité
$\\leq 2^{-41} \\approx 4.5 \\times 10^{-13}$, ce qui la rend impraticable en pratique.

Le temps de résolution croît exponentiellement avec $R$ (axe log à droite), ce qui motive
l'utilisation de techniques plus avancées pour $R > 10$.
"""))

cells.append(code("""\
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

ax = axes[0]
ax.plot(R_vals, [min_active_results[r] for r in R_vals], 'o-', label='min actives')
ax.plot(R_vals, [2 * min_active_results[r] for r in R_vals], '--', alpha=0.5, label='2 × actif')
ax.plot(R_vals, [min_weight_results[r] for r in R_vals], 's-', label='min poids')
ax.set_xlabel('tours')
ax.set_ylabel('valeur')
ax.set_title('S-boxes actives vs poids du chemin')
ax.legend()
ax.grid(alpha=0.3)

ax = axes[1]
ax.semilogy(R_vals, [solve_times[r] for r in R_vals], 'o-')
ax.set_xlabel('tours')
ax.set_ylabel('temps (s)')
ax.set_title('Temps de résolution SAT (log)')
ax.grid(alpha=0.3, which='both')

plt.tight_layout()
plt.show()
"""))

cells.append(code("""\
R_vis = 5
W_vis = min_weight_results[R_vis]
cnf_vis = build_weighted_model(R_vis, W=W_vis)

with Cadical153(bootstrap_with=cnf_vis) as solver:
    solver.solve()
    model = solver.get_model()
    deltas_vis = [
        sum((1 << i) for i in range(64) if model[diff_var(r, i) - 1] > 0)
        for r in range(R_vis + 1)
    ]
    is_w2 = [[model[w2_var(R_vis, r, s) - 1] > 0 for s in range(16)] for r in range(R_vis)]
    is_w3 = [[model[w3_var(R_vis, r, s) - 1] > 0 for s in range(16)] for r in range(R_vis)]

fig, ax = plt.subplots(figsize=(14, 4))
ax.set_xlim(-0.5, 15.5)
ax.set_ylim(-0.5, R_vis + 0.5)
ax.set_aspect('equal')
ax.invert_yaxis()

for r in range(R_vis + 1):
    d = deltas_vis[r]
    for s in range(16):
        nibble = (d >> (4 * s)) & 0xF
        if r < R_vis:
            color = 'steelblue' if is_w2[r][s] else ('tomato' if is_w3[r][s] else '#eee')
        else:
            color = '#aad' if nibble else '#eee'
        ax.add_patch(plt.Rectangle((s - 0.45, r - 0.45), 0.9, 0.9,
                                    fc=color, ec='gray', lw=0.5))
        if nibble:
            ax.text(s, r, f'{nibble:X}', ha='center', va='center',
                    fontsize=8, color='white' if color not in ('#eee', '#aad') else '#333')

ax.set_xticks(range(16))
ax.set_xticklabels([f'S{i}' for i in range(16)], fontsize=8)
ax.set_yticks(range(R_vis + 1))
ax.set_yticklabels([f'd{r}' for r in range(R_vis + 1)])
ax.set_title(f'Chemin optimal R=5 (poids={W_vis})')
ax.legend(handles=[
    plt.Rectangle((0, 0), 1, 1, fc='steelblue', label='poids 2 (DDT=4)'),
    plt.Rectangle((0, 0), 1, 1, fc='tomato',    label='poids 3 (DDT=2)'),
    plt.Rectangle((0, 0), 1, 1, fc='#eee', ec='gray', label='inactif'),
], loc='upper right')
plt.tight_layout()
plt.show()

w2 = sum(is_w2[r][s] for r in range(R_vis) for s in range(16))
w3 = sum(is_w3[r][s] for r in range(R_vis) for s in range(16))
print(f"poids 2 : {w2}, poids 3 : {w3}, total : {2*w2 + 3*w3}")
"""))

# ── 7. Conclusion ────────────────────────────────────────────────────────────
cells.append(md("""\
## 7. Conclusion

### Ce qu'on a fait

On a encodé la recherche de chemins différentiels de poids minimum sur PRESENT en SAT, en
exploitant trois optimisations cumulatives :

1. **Solver incrémental** — on réutilise les clauses apprises entre les itérations de la
   recherche binaire, au lieu de relancer le solver depuis zéro à chaque étape.
2. **Étape optimiste** (`w3=False`) — on prouve que forcer toutes les transitions à
   $\\text{DDT}=4$ est équivalent à chercher un chemin de poids $\\leq 2K$, ce qui réduit
   l'espace d'un facteur $4\\times$ par S-box.
3. **Portfolio** — trois solveurs CDCL tournent en parallèle sur l'instance la plus difficile ;
   on retourne dès que l'un d'eux répond.

### Résultats

| propriété | valeur |
|---|---|
| $\\text{min\\_active}(5)$ | $10$ — confirme Bogdanov et al. Theorem 1 |
| $\\text{min\\_weight}(R=1..9)$ | $= 2 \\times \\text{min\\_active}$ (borne atteinte) |
| $\\text{min\\_weight}(10)$ | $41 > 40$ — gap : une transition $\\text{DDT}=2$ est forcée |
| prob. max attaque 10 tours | $\\leq 2^{-41} \\approx 4.5 \\times 10^{-13}$ (impraticable) |

### Limites et perspectives

Le temps de résolution SAT croît exponentiellement avec $R$ : $\\sim 130$ s pour $R=10$,
impraticable au-delà. La cause est structurelle : CDCL est un solveur généraliste qui ne
connaît pas la monotonie du poids ou la structure S-box/P-layer.

Une approche DFS branch-and-bound avec élagage PC1/PC2 (Kim et al., ToSC 2022) exploite
ces propriétés explicitement et atteint $R=31$ en quelques secondes en C — même algorithme
de recherche, mais avec des bornes inférieures $B[r]$ calculées inductivement.
"""))

# ── write ─────────────────────────────────────────────────────────────────────
nb = nbformat.v4.new_notebook()
nb['cells'] = cells
nb['metadata'] = {
    'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
    'language_info': {'name': 'python', 'version': '3.11.0'},
}

with open('notebook.ipynb', 'w') as f:
    nbformat.write(nb, f)

print(f"written {len(cells)} cells → notebook.ipynb")
