# PRESENT Differential Trail Search - SAT Encoding

Projet F2 du cours **Programmation par Contraintes** (EPITA SCIA 2026).

Recherche automatique de trajectoires différentielles optimales sur le chiffrement par blocs [PRESENT](papers/1-present-an-ultralightweight-block-cipher.pdf) via encodage SAT (CNF), en utilisant les solveurs CaDiCaL et Kissat.

## But

La cryptanalyse différentielle cherche comment des différences entre paires de textes clairs se propagent à travers les tours d'un chiffrement. Trouver la trajectoire de poids minimal (probabilité d'attaque maximale) est un problème NP-difficile qu'on ramène ici à de la satisfiabilité propositionnelle :

- chaque tour de PRESENT est encodé en clauses CNF (S-box via table DDT, permutation de bits) ;
- un solveur SAT cherche une affectation correspondant à une trajectoire différentielle valide ;
- une recherche incrémentale ou binaire sur le poids trouve le minimum global.

## Structure

```
present_sat/
├── present.py     - implémentation de PRESENT (S-box, DDT, permutation de bits)
├── encoding.py    - construction du modèle CNF (clauses DDT, poids, décodage de trail)
├── search.py      - recherche du minimum (S-box actives via dichotomie, poids de trail via recherche linéaire)
├── display.py     - affichage live en terminal + rendu des benchmarks
└── main.py        - point d'entrée CLI
notebook.ipynb     - analyse, visualisations et résultats
benchmark.json     - résultats pré-calculés (kissat-seq, kissat, cadical, R=1..31)
papers/            - articles de référence
images/            - schémas et images du notebook
```

## Installation

```bash
uv sync
```

## Utilisation

```bash
# Nombre minimum de S-box actives, rounds 1 à 10
uv run python -m present_sat --rmin 1 --rmax 31 --active

# Poids minimum de trail (mode par défaut : borne inférieure = 2 * min_active)
uv run python -m present_sat --weight

# Poids minimum de trail en mode kissat-seq : chaque round utilise weight[R-1] comme borne inférieure
uv run python -m present_sat --weight --seq

# Puisque le flag --seq ne permet pas de parallèliser les calculs (le calcul de weight[R] doit attendre que 
# celui de wegith[R-1] soit fini), le flag --cache utilise la même optimisation de la borne inférieur mais
# récupère les valeurs de weight[R-1] à dans la cache.
uv run python -m present_sat --weight --cache

# Trail complet avec affichage, en parallèle avec le solveur kissat
uv run python -m present_sat --trail --solver cadical

# Choisir le nombre de workers (défaut : cpu_count // 3)
uv run python -m present_sat --weight --workers 4

# Afficher les résultats sauvegardés
uv run python -m present_sat --benchmark
uv run python -m present_sat --benchmark chemin/vers/autre.json
```

### Options

| Option | Description |
|---|---|
| `--rmin`, `--rmax` | Plage de rounds à analyser (défaut : 1–10) |
| `--active` | Calcule le nombre minimum de S-box actives |
| `--weight` | Calcule le poids minimum du meilleur trail |
| `--trail` | Extrait et affiche un trail différentiel optimal |
| `--seq` | Séquentiel (kissat-seq) : utilise `weight[R-1]` comme borne inférieure pour `weight[R]` |
| `--cached` | Parallèle : passe `weight[R-1]` comme borne dès qu'il est disponible |
| `--solver` | `kissat` (défaut) ou `cadical` |
| `--workers` | Nombre de processus parallèles (défaut : `cpu_count // 3`) |
| `--benchmark` | Affiche les résultats de `benchmark.json` (chemin optionnel) |

**Note sur les bornes inférieures :** sans `--seq` ni `--cached`, la borne de départ est `2 * min_active[R]`. Avec `--seq` ou `--cached`, `weight[R-1]` est utilisé comme borne, ce qui permet de démarrer la recherche linéaire nettement plus haut et réduit significativement le temps de calcul.

## Résultats

Les résultats obtenus sont les même que ceux décrit par la littérature (voir le dossier papers et le [notebook](notebook.ipynb)). Le benchmark complet (`benchmark.json`) couvre les rounds 1–31 avec les trois configurations : kissat-seq, kissat et cadical. Le seuil de sécurité différentielle (`w_min > 64`) est atteint à **R=16**.

## Références

- [PRESENT: An Ultra-Lightweight Block Cipher](papers/1-present-an-ultralightweight-block-cipher.pdf) - description complète du chiffrement : S-box, permutation de bits, DDT ; base de l'implémentation.
- [A Tutorial on Linear and Differential Cryptanalysis](papers/2-a-tutorial-on-linear-and-differential-cryptanalysis.pdf) - introduction à la cryptanalyse différentielle ; propagation des différences et probabilités de trail.
- [Differential Cryptanalysis of Reduced-Round PRESENT](papers/3-differential-cryptanalysis-of-reducedround-present.pdf) - introduction à la cryptanalyse différentielle de PRESENT.
- [Accelerating the Best Trail Search on AES-like Ciphers](papers/4-accelerating-the-best-trail-search-on-aes-like-ciphers.pdf) - résultats de référence sur les poids minimaux de trails pour PRESENT ; valeurs cibles pour valider l'encodage SAT.
- [Improving the MILP-based Security Evaluation Algorithm against Differential Cryptanalysis](papers/5-improving-the-MILP-based-security-evaluation-algorithm-against-differential-cryptanalysis.pdf) - résultats de référence sur le nombre minimum de S-boxes actives pour PRESENT.
