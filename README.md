# EPITA 2026 — Programmation par Contraintes

## Liste des sujets de projet

Ce document presente les sujets de projet pour le cours de Programmation par Contraintes (SCIA). Chaque sujet inclut une description detaillee, des references academiques et pratiques, des liens vers des ressources de bootstrapping (tutoriels, notebooks, benchmarks), et les technologies pertinentes.

> **Consignes de choix** : Chaque groupe doit forker ce depot et creer un dossier pour son projet contenant le code source, un notebook explicatif une UI ou une démo, et les slides de soutenance. Les livraisons se font via des pull requests regulieres idéalement.

---

## Modalites du projet

### Taille des groupes

| Taille            | Bonus/Malus |
| ----------------- | ----------- |
| 3 personnes       | Standard    |
| 2 personnes       | +1 point    |
| 1 personne (solo) | +3 points   |
| 4 personnes       | -1 point    |

### Bonus de TP

2 TPs rendus dans le semestre. Pour chaque TP :

- 0.5 point de bonus par exercice supplementaire rendu au-dela du minimum requis
- **1 point de bonus max par TP**, soit **2 points de bonus TP max au total**

Ces points s'ajoutent a la note de projet.

### Soutenance — Evaluation collegiale

La soutenance finale est evaluee de maniere **collegiale** (pairs + enseignants). Chaque groupe est note sur **4 criteres** (0-10 chacun) :

| Critere                        | Description                                                                                                        |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| **Qualite de la presentation** | Communication, clarte, pedagogie, qualite des slides, demonstrations                                               |
| **Qualite theorique**          | Principes CP/CSP utilises, classes d'algorithmes, contexte historique, explication des performances et limitations |
| **Qualite technique**          | Livrables (code, notebook, UI), qualite du code, commits Git, demonstrations, resultats, perspectives              |
| **Organisation**               | Planning, repartition des taches, collaboration, activite Git, documentation                                       |

**Note finale = somme des 4 criteres / 2 (echelle /20), ajustee du bonus/malus taille de groupe et des bonus TP.**

### Livrables attendus

- **Code source** documente dans un sous-dossier dedie (`groupe-XX-nom-sujet/`)
- **Notebook Jupyter** explicatif avec analyse et visualisations **OU** **UI/demo fonctionnelle** (au choix — un notebook tres complet peut tenir lieu de demo, et inversement)
- **Slides de soutenance** (PDF ou lien)
- **Pull Request** soumise au plus tard **2 jours avant la soutenance**

### Echeances

- **Date de soutenance** : en cours de confirmation avec la scolarite
- **Deadline PR** : 2 jours avant la soutenance

---

## Ressources communes a tous les sujets

### Solveurs et outils

- **Google OR-Tools CP-SAT** : le solveur de reference pour ce cours. [Documentation officielle](https://developers.google.com/optimization/cp/cp_solver), [Guide Python](https://developers.google.com/optimization/cp/introduction), [Exemples par probleme](https://github.com/google/or-tools/tree/stable/examples/python)
- **Z3 SMT Solver** : pour les problemes de verification et de raisonnement symbolique. [Documentation](https://z3prover.github.io/api/html/namespacez3py.html), [Tutoriel Python](https://ericpony.github.io/z3py-tutorial/guide-examples.htm)
- **MiniZinc** : langage de modelisation CP de haut niveau. [Tutoriel](https://www.minizinc.org/doc-2.5.5/en/), [Benchmarks](https://www.minizinc.org/challenge.html)
- **CPMpy** : interface Python pour CP avec backends multiples. [Documentation](https://cpmpy.readthedocs.io/), [Exemples](https://github.com/CPMpy/cpmpy/tree/master/examples)

### Benchmarks et instances

- **CSPLib** : bibliotheque de problemes CP de reference. [En ligne](https://www.csplib.org/)
- **OR-Library** : instances pour problemes d'OR. [Beasley OR-Library](http://people.brunel.ac.uk/~mastjjb/jeb/info.html)
- **MiniZinc Challenge Benchmarks** : instances de competition. [GitHub](https://github.com/minizinc/minizinc-benchmarks)

### Notebooks du cours CoursIA

Les notebooks suivants sont disponibles dans le depot CoursIA ([jsboige/CoursIA](https://github.com/jsboige/CoursIA)) et constituent des prerequis ou des points de depart pour les projets :

- **Search/Part1-Foundations/** : Search-1 (StateSpace), Search-3 (A\*, heuristiques), Search-4 (Local Search), Search-9 (Programmation lineaire), Search-11 (Metaheuristiques)
- **Search/Part2-CSP/** : CSP-1 (Fondamentaux), CSP-4 (Scheduling, IntervalVar, NoOverlap, Cumulative), CSP-5 (Optimization, Bin Packing, Knapsack), CSP-6 (Hybridation CP+SAT, LLM+CSP), CSP-7 (Soft Constraints), CSP-9 (Distributed CSP)
- **Search/Applications/CSP/** : App-4 (Job-Shop Scheduling), App-8 (MiniZinc), App-11 (Picross)
- **Search/Applications/Hybrid/** : App-10 (Portfolio Optimization), App-13 (TSP Metaheuristics), App-17 (VRP avec SA, GA, ACO, CP-SAT)
- **SymbolicAI/SmartContracts/** : Serie de 27 notebooks (SC-0 a SC-26) couvrant blockchain, Solidity, verification formelle (SC-14), fuzz testing (SC-13), cryptographie ZKP/HE (SC-15/16)
- **SymbolicAI/Planners/** : Planners-1 a Planners-12 couvrant PDDL, Fast Downward, planification temporelle, HTN, LLM Planning
- **SymbolicAI/Linq2Z3.ipynb** : Z3 SMT Solver en C#
- **SymbolicAI/OR-tools-Stiegler.ipynb** : OR-Tools CP en C#
- **Sudoku/** : 18 notebooks couvrant Sudoku avec multiples solveurs (Z3, CP-SAT, backtracking)
- **GameTheory/** : 17+ notebooks couvrant Nash Equilibrium, Cooperative Games, Shapley Value, Mechanism Design
- **Integration LLM** : function calling avec OpenAI/MCP pour assister la modelisation CP. Voir [Function Calling - OpenAI](https://platform.openai.com/docs/guides/function-calling) et [MCP Specification](https://modelcontextprotocol.io/)

---

### Categorie F : SAT/SMT Industriel

| #                                                               | Sujet                                               | Difficulte |
| --------------------------------------------------------------- | --------------------------------------------------- | ---------- |
| [F1](#f1---model-checking-hardware-par-sat-ic3pdr)              | Model checking hardware par SAT (IC3/PDR)           | 4/5        |
| [F2](#f2---cryptanalyse-differentielle-par-sat)                 | Cryptanalyse differentielle par SAT                 | 4/5        |
| [F3](#f3---bounded-model-checking-de-programmes-c)              | Bounded Model Checking de programmes C              | 3/5        |
| [F4](#f4---compiler-fuzzing-par-generation-smt-dinputs)         | Compiler fuzzing par generation SMT d'inputs        | 4/5        |
| [F5](#f5---verification-smt-de-reseaux-de-regulation-genetique) | Verification SMT de reseaux de regulation genetique | 3/5        |

---

## F2 - Cryptanalyse differentielle par SAT

La cryptanalyse differentielle est une technique qui etudie comment les differences entre paires de textes clairs se propagent a travers les tours d'un chiffrement par blocs (AES, DES,PRESENT). L'encodage SAT de cette propagation permet de chercher automatiquement les trajectoires differentielles optimales (celles qui maximisent la probabilite de succes d'une attaque). Chaque tour du chiffrement est encode comme un ensemble de clauses CNF, et le solveur SAT cherche une affectation qui correspond a une trajectoire differentielle valide.

### Objectifs

- Encoder la propagation differentielle d'un chiffrement par blocs (PRESENT, Skinny, ou AES reduit) en SAT (CNF)
- Implementer la recherche de trajectoires differentielles optimales avec un solveur SAT (CaDiCaL ou Kissat)
- Ajouter des contraintes sur la probabilite cumulee et le nombre de tours actifs
- Evaluer sur des chiffrements de la litterature avec des cles reduites (nombre de tours limite)
- Comparer les resultats avec les trajectoires differentielles connues dans la litterature cryptographique

### Notebooks CoursIA pertinents

| Notebook                 | Chemin                                                                                                                                                                                                                                    | Pertinence       |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- |
| Linq2Z3                  | [SymbolicAI/Linq2Z3.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Linq2Z3.ipynb)                                                                                                                       | SAT/SMT solving  |
| CSP-1 Fondamentaux       | [Search/Part2-CSP/CSP-1-Fundamentals.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-1-Fundamentals.ipynb)                                                                                     | Modelisation CSP |
| CSP-6 Hybridation CP+SAT | [Search/Part2-CSP/CSP-6-Hybridization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-6-Hybridization.ipynb)                                                                                   | SAT encoding     |
| SC-15 Cryptography ZKP   | [SymbolicAI/SmartContracts/04-Privacy-Cryptography/SC-15-Zero-Knowledge-Proofs.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/SmartContracts/04-Privacy-Cryptography/SC-15-Zero-Knowledge-Proofs.ipynb) | Cryptographie    |

### References externes

- Biere, A. (2021). "CaDiCaL, Kissat MAB and Mate at the SAT Competition 2021." _SAT Competition_. [dblp](https://dblp.org/rec/conf/sat/BiereF21)
- Mouha, N., & Preneel, B. (2013). "Towards Finding Optimal Differential Characteristics for ARX." _FSE_. [IACR](https://eprint.iacr.org/2013/328)
- Sun, S., et al. (2013). "Automatic Security Evaluation and (Related-Key) Differential Characteristic Search: Application to SIMON, PRESENT, LBlock, DES(L) and Other Bit-Oriented Block Ciphers." _ASIACRYPT_. [IACR](https://eprint.iacr.org/2013/676)
- Bogdanov, A., et al. (2007). "PRESENT: An Ultra-Lightweight Block Cipher." _CHES_. [Springer](https://doi.org/10.1007/978-3-540-74735-2_31)

### Difficulte : 4/5

## Annexe : Sujets interdits (anti-plagiat)

Les sujets suivants ont ete traites dans des editions precedentes (EPITA 2025, EPF, ECE) et sont **strictement interdits** pour cette edition 2026. Toute reprise, meme sous forme de variante avancee, sera consideree comme du plagiat.

1. Nurse Rostering Problem (EPITA 2025)
2. Job-Shop Scheduling basique (EPITA 2025)
3. Student Project Allocation / Stable Marriage classique (EPITA 2025)
4. Picross Solver (EPITA 2025)
5. Constraint-Based City Generation (EPITA 2025)
6. Sports Tournament Scheduling (EPITA 2025)
7. Tourist Itinerary Planner (EPITA 2025)
8. Sudoku Solver (EPITA 2025 + CoursIA)
9. CSP Wordle Solver (EPITA 2025 + EPF + ECE)
10. Mots-croises / Crossword CSP (EPITA 2025 + EPF + ECE)
11. Quoridor (EPITA 2025)
12. Multi-robot Warehouse Task Assignment (EPITA 2025)
13. Product Configuration sous contraintes (EPITA 2025)
14. Timetabling / Emploi du temps (EPITA 2025 + EPF + ECE)
15. Minesweeper / Demineur CSP (EPITA 2025 + EPF + ECE)
16. Portfolio Optimization classique (EPITA 2025)
17. Graph Coloring basique (ECE)
18. Satellite Capture Scheduler (EPITA 2025)
19. Automatic Tests Generation basique (EPITA 2025)
20. VRP classique / Vehicle Routing Problem (EPF Min1)

**Note :** Si un sujet de cette liste vous interesse, vous pouvez le proposer comme base dans une categorie L (Competition) si vous apportez une contribution technique significative (nouvelle heuristique, nouveau modele, benchmark original). Contactez l'equipe pedagogique pour validation prealable.

---

_Derniere mise a jour : Avril 2026_
_Contact : Equipe pedagogique Programmation par Contraintes, EPITA SCIA_
