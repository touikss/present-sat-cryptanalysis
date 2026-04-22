# EPITA 2026 — Programmation par Contraintes

## Liste des sujets de projet

Ce document presente les sujets de projet pour le cours de Programmation par Contraintes (SCIA). Chaque sujet inclut une description detaillee, des references academiques et pratiques, des liens vers des ressources de bootstrapping (tutoriels, notebooks, benchmarks), et les technologies pertinentes.

> **Consignes de choix** : Chaque groupe doit forker ce depot et creer un dossier pour son projet contenant le code source, un notebook explicatif une UI ou une démo, et les slides de soutenance. Les livraisons se font via des pull requests regulieres idéalement.

---

## Modalites du projet

### Taille des groupes

| Taille | Bonus/Malus |
|--------|-------------|
| 3 personnes | Standard |
| 2 personnes | +1 point |
| 1 personne (solo) | +3 points |
| 4 personnes | -1 point |

### Bonus de TP

2 TPs rendus dans le semestre. Pour chaque TP :
- 0.5 point de bonus par exercice supplementaire rendu au-dela du minimum requis
- **1 point de bonus max par TP**, soit **2 points de bonus TP max au total**

Ces points s'ajoutent a la note de projet.

### Soutenance — Evaluation collegiale

La soutenance finale est evaluee de maniere **collegiale** (pairs + enseignants). Chaque groupe est note sur **4 criteres** (0-10 chacun) :

| Critere | Description |
|---------|-------------|
| **Qualite de la presentation** | Communication, clarte, pedagogie, qualite des slides, demonstrations |
| **Qualite theorique** | Principes CP/CSP utilises, classes d'algorithmes, contexte historique, explication des performances et limitations |
| **Qualite technique** | Livrables (code, notebook, UI), qualite du code, commits Git, demonstrations, resultats, perspectives |
| **Organisation** | Planning, repartition des taches, collaboration, activite Git, documentation |

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
- **Search/Part1-Foundations/** : Search-1 (StateSpace), Search-3 (A*, heuristiques), Search-4 (Local Search), Search-9 (Programmation lineaire), Search-11 (Metaheuristiques)
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

## Index des Sujets

### Categorie A : Sante, Social et Sciences du Vivant

| # | Sujet | Difficulte |
|---|-------|------------|
| [A1](#a1---echange-de-reins-kidney-exchange) | Echange de reins (Kidney Exchange) | 3/5 |
| [A2](#a2---planification-nutritionnelle-diet-problem) | Planification nutritionnelle (DIET Problem) | 2/5 |
| [A3](#a3---ordonnancement-de-blocs-operatoires) | Ordonnancement de blocs operatoires | 3/5 |
| [A4](#a4---optimisation-stochastique-de-protocoles-pharmaceutiques) | Optimisation stochastique de protocoles pharmaceutiques | 4/5 |

### Categorie B : Production et Chaine Logistique

| # | Sujet | Difficulte |
|---|-------|------------|
| [B1](#b1---equilibrage-de-chaine-dassemblage-salbp) | Equilibrage de chaine d'assemblage (SALBP) | 3/5 |
| [B2](#b2---conception-de-chaine-logistique-supply-chain-network-design) | Conception de chaine logistique (Supply Chain Network Design) | 3/5 |
| [B3](#b3---chargement-de-conteneurs-bin-packing-3d) | Chargement de conteneurs (Bin Packing 3D) | 3/5 |
| [B4](#b4---ordonnancement-industriel-rcpsp) | Ordonnancement industriel (RCPSP) | 3/5 |

### Categorie C : Mobilite et Tournees Vertes

| # | Sujet | Difficulte |
|---|-------|------------|
| [C1](#c1---tournees-de-livraison-vertes-electric-vrp) | Tournees de livraison vertes (Electric VRP) | 3/5 |
| [C2](#c2---ordonnancement-ferroviaire-railway-timetabling) | Ordonnancement ferroviaire (Railway Timetabling) | 4/5 |
| [C3](#c3---livraison-par-drones-drone-delivery-routing) | Livraison par drones (Drone Delivery Routing) | 3/5 |
| [C4](#c4---assemblage-orbital-de-satellites-orbital-assembly-scheduling) | Assemblage orbital de satellites (Orbital Assembly Scheduling) | 4/5 |

### Categorie D : Cloud, Edge et Energie

| # | Sujet | Difficulte |
|---|-------|------------|
| [D1](#d1---allocation-de-ressources-cloud-vm-scheduling) | Allocation de ressources cloud (VM Scheduling) | 3/5 |
| [D2](#d2---optimisation-energetique-de-centres-de-donnees) | Optimisation energetique de centres de donnees | 3/5 |
| [D3](#d3---placement-de-services-en-edge-computing) | Placement de services en edge computing | 3/5 |
| [D4](#d4---dispatch-dans-un-reseau-electrique) | Dispatch dans un reseau electrique | 4/5 |

### Categorie E : Blockchain et Cryptographie

| # | Sujet | Difficulte |
|---|-------|------------|
| [E1](#e1---super-optimisation-gas-solidity-par-max-smt) | Super-optimisation gas Solidity par Max-SMT | 4/5 |
| [E2](#e2---ordonnancement-mev-resistant-de-transactions) | Ordonnancement MEV-resistant de transactions | 3/5 |
| [E3](#e3---synthese-de-circuits-zero-knowledge-sous-contraintes) | Synthese de circuits Zero-Knowledge sous contraintes | 4/5 |
| [E4](#e4---allocation-de-validators-pos-par-bin-packing) | Allocation de validators PoS par bin-packing | 3/5 |
| [E5](#e5---verification-formelle-smt-de-vulnerabilites-solidity) | Verification formelle SMT de vulnerabilites Solidity | 3/5 |

### Categorie F : SAT/SMT Industriel

| # | Sujet | Difficulte |
|---|-------|------------|
| [F1](#f1---model-checking-hardware-par-sat-ic3pdr) | Model checking hardware par SAT (IC3/PDR) | 4/5 |
| [F2](#f2---cryptanalyse-differentielle-par-sat) | Cryptanalyse differentielle par SAT | 4/5 |
| [F3](#f3---bounded-model-checking-de-programmes-c) | Bounded Model Checking de programmes C | 3/5 |
| [F4](#f4---compiler-fuzzing-par-generation-smt-dinputs) | Compiler fuzzing par generation SMT d'inputs | 4/5 |
| [F5](#f5---verification-smt-de-reseaux-de-regulation-genetique) | Verification SMT de reseaux de regulation genetique | 3/5 |

### Categorie G : Planification sous Contrainte

| # | Sujet | Difficulte |
|---|-------|------------|
| [G1](#g1---planification-temporelle-pddl-21--cp-hybride) | Planification temporelle PDDL 2.1 + CP hybride | 4/5 |
| [G2](#g2---planification-htn-sous-contraintes) | Planification HTN sous contraintes | 4/5 |
| [G3](#g3---coordination-de-drones-par-multi-agent-path-finding) | Coordination de drones par Multi-Agent Path Finding | 3/5 |
| [G4](#g4---apprentissage-dheuristiques-pour-solveurs-cp) | Apprentissage d'heuristiques pour solveurs CP | 4/5 |

### Categorie H : Jeux, Art et Puzzles Avances

| # | Sujet | Difficulte |
|---|-------|------------|
| [H1](#h1---composition-musicale-assistee-par-contraintes) | Composition musicale assistee par contraintes | 3/5 |
| [H2](#h2---generation-procedurale-de-niveaux-de-jeu) | Generation procedurale de niveaux de jeu (WFC) | 3/5 |
| [H3](#h3---cryptanalyse-par-contraintes-ciphers-avances) | Cryptanalyse par contraintes (ciphers avances) | 3/5 |
| [H4](#h4---covering-arrays-avec-contraintes-semantiques) | Covering Arrays avec contraintes semantiques | 3/5 |

### Categorie I : LLM + CSP Hybride

| # | Sujet | Difficulte |
|---|-------|------------|
| [I1](#i1---assistant-de-planification-conversationnel-llm--csp) | Assistant de planification conversationnel (LLM + CSP) | 3/5 |
| [I2](#i2---explicateur-de-solutions-cp-par-llm) | Explicateur de solutions CP par LLM | 3/5 |
| [I3](#i3---modelisation-cp-assistee-par-llm) | Modelisation CP assistee par LLM | 4/5 |

### Categorie J : RH, Matching et Mechanism Design

| # | Sujet | Difficulte |
|---|-------|------------|
| [J1](#j1---allocation-multicritere-de-candidats) | Allocation multicritere de candidats | 3/5 |
| [J2](#j2---enchere-combinatoire-et-winner-determination) | Enchere combinatoire et Winner Determination | 4/5 |
| [J3](#j3---allocation-de-ressources-par-mecanisme-incitatif) | Allocation de ressources par mecanisme incitatif | 4/5 |

### Categorie K : Urbanisme, Environnement et Multi-criteres

| # | Sujet | Difficulte |
|---|-------|------------|
| [K1](#k1---planification-urbaine-et-placement-dinfrastructures) | Planification urbaine et placement d'infrastructures | 3/5 |
| [K2](#k2---allocation-de-frequences-radio) | Allocation de frequences radio | 3/5 |
| [K3](#k3---optimisation-multiobjectif-sous-contraintes) | Optimisation multiobjectif sous contraintes | 4/5 |

### Categorie L : Competitions et Benchmarks

| # | Sujet | Difficulte |
|---|-------|------------|
| [L1](#l1---participation-a-une-competition-cpsatsmt) | Participation a une competition CP/SAT/SMT | Variable |

### Categorie M : Finance Quantitative et Trading Algorithmique

| # | Sujet | Difficulte |
|---|-------|------------|
| [M1](#m1---portefeuille-parcimonieux-sous-contraintes-de-cardinalite-sparse-markowitz) | Portefeuille parcimonieux sous contraintes de cardinalite (Sparse Markowitz) | 3/5 |
| [M2](#m2---replication-dindice-sous-contraintes-sparse-index-tracking) | Replication d'indice sous contraintes (Sparse Index Tracking) | 3/5 |
| [M3](#m3---selection-de-paires-pour-stat-arb-par-enumeration-de-cliques-cp) | Selection de paires pour stat-arb par enumeration de cliques (CP) | 4/5 |
| [M4](#m4---execution-optimale-dordres-twapvwap-avec-impact-de-marche) | Execution optimale d'ordres (TWAP/VWAP avec impact de marche) | 4/5 |
| [M5](#m5---allocation-risk-parity-sous-contraintes-de-cardinalite) | Allocation Risk-Parity sous contraintes de cardinalite | 4/5 |
| [M6](#m6---arbitrage-triangulaire-crypto-par-detection-de-cycles-cp--bellman-ford) | Arbitrage triangulaire crypto par detection de cycles (CP + Bellman-Ford) | 3/5 |

> **Note** : Les sujets de la categorie M sont **specifiquement orientes vers la programmation par contraintes** appliquee au trading algorithmique. Ils exigent une modelisation CP-SAT / MiniZinc / CPMpy ou Z3 OMT (pas seulement du ML ou du backtesting pur). Chaque projet **doit** etre valide par un backtest sur la plateforme [QuantConnect Lean](https://www.quantconnect.com/) grace au partenariat educatif sponsorise par Jared Broad (CEO QC). Les etudiants ayant rejoint l'organisation QuantConnect sponsorisee sont encourages a choisir en priorite ces sujets.
>
> **Attention** : La **Portfolio Optimization classique de Markowitz** est listee dans l'[annexe anti-plagiat](#annexe--sujets-interdits-anti-plagiat) (traitee en EPITA 2025). Les sujets M1-M5 sont des **extensions combinatoires** (cardinalite, lots entiers, scheduling, cout d'execution, robustesse) qui n'ont jamais ete couvertes auparavant.

---

## A1 - Echange de reins (Kidney Exchange)

Le Kidney Exchange Problem (KEP) consiste a trouver des cycles d'echanges de reins entre des paires patient-donneur incompatibles, de maniere a maximiser le nombre de transplantations realisables. Ce probleme, issu de la recherche operationnelle appliquee a la sante, se modelise naturellement comme un probleme de couverture par cycles disjoints dans un graphe oriente value. Les contraintes portent sur la compatibilite immunologique, la taille maximale des cycles (limitee par des considerations logistiques), et l'equite dans l'allocation. C'est un sujet ideal pour explorer la programmation par contraintes appliquee a un probleme concret a fort impact social.

### Objectifs
- Modeliser le KEP comme un probleme de recherche de cycles disjoints dans un graphe oriente avec CP-SAT
- Implementer les contraintes de compatibilite immunologique (sang, tissu, anticorps) et de taille de cycle
- Comparer les performances de CP-SAT avec une approche PLNE et une heuristique gloutonne
- Etendre le modele pour inclure des chaines altruistes (chains initiated by non-directed donors)
- Evaluer sur des instances reelles du dataset UNOS ou des benchmarks synthetiques

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-1 Fondamentaux | [Search/Part2-CSP/CSP-1-Fundamentals.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-1-Fundamentals.ipynb) | Modelisation CSP de base |
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Knapsack, allocation sous contraintes |
| GameTheory - Cooperative | [GameTheory/](https://github.com/jsboige/CoursIA/tree/main/MyIA.AI.Notebooks/GameTheory) | Shapley Value, allocation equitable |
| Search-1 StateSpace | [Search/Part1-Foundations/Search-1-StateSpace.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-1-StateSpace.ipynb) | Graphes d'etat, parcours |

### References externes
- Abraham, D.J., Blum, A., & Sandholm, T. (2007). "Clearing Algorithms for Barter Exchange Markets: Enabling Nationwide Kidney Exchanges." *EC'07*. [ACM DL](https://dl.acm.org/doi/10.1145/1250910.1250954)
- Dickerson, J.P. & Sandholm, T. (2012). "Dynamic Matching via Weighted Myopia with Application to Kidney Exchange." *AAAI*. [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/8252)
- UNOS Kidney Paired Donation Program. [unos.org](https://unos.org/transplant/kidney-paired-donation/)
- Mak-Hau, V. (2017). "On the Kidney Exchange Problem: Tighter IP Formulations." *European Journal of Operational Research*. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0377221717305760)
- CSPLib Problem 047: Kidney Exchange. [csplib.org](https://www.csplib.org/Problems/prob047/)

### Difficulte : 3/5

---

## A2 - Planification nutritionnelle (DIET Problem)

Le Diet Problem est un classique de la recherche operationnelle : determiner la combinaison d'aliments la moins coutee satisfaisant l'ensemble des besoins nutritionnels journaliers. Modelisable comme un programme lineaire en nombres entiers (Knapsack multi-dimensionnel), il se prete remarquablement a une modelisation CP-SAT avec des contraintes sur les calories, proteines, lipides, glucides, vitamines et mineraux. Le sujet s'etend naturellement vers la generation de menus hebdomadaires equilibres en ajoutant des contraintes de variete (ne pas manger le meme plat deux jours de suite), de saisonnalite, de budget, et de preferences alimentaires.

### Objectifs
- Modeliser le Diet Problem comme un knapsack multi-dimensionnel avec CP-SAT (variables binaires par aliment, contraintes nutritionnelles)
- Etendre le modele en planification de menus hebdomadaires avec contraintes de variete, budget et saisonnalite
- Integrer des preferences utilisateur comme soft constraints avec penalites ponderees
- Benchmarker sur les donnees USDA FoodData Central et les apports nutritionnels OMS/ANSES
- Comparer l'approche CP-SAT avec une resolution PLNE classique (OR-Tools linear solver)

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Knapsack, Bin Packing, optimisation |
| CSP-7 Soft Constraints | [Search/Part2-CSP/CSP-7-Soft.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-7-Soft.ipynb) | Penalites, preferences, compromis |
| Search-9 Programmation lineaire | [Search/Part1-Foundations/Search-9-LinearProgramming.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-9-LinearProgramming.ipynb) | PLNE, simplex, dualite |
| App-10 Portfolio Optimization | [Search/Applications/Hybrid/App-10-Portfolio.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Applications/Hybrid/App-10-Portfolio.ipynb) | Optimisation sous contraintes de budget |

### References externes
- Stigler, G.J. (1945). "The Cost of Subsistence." *Journal of Farm Economics*, 27(2), 303-314. [JSTOR](https://www.jstor.org/stable/1231810)
- USDA FoodData Central. [fdc.nal.usda.gov](https://fdc.nal.usda.gov/)
- ANSES - Apports nutritionnels conseilles. [anses.fr](https://www.anses.fr/en/content/nutrition)
- Briend, A., et al. (2020). "Modelling the Cost of a Diet: A Review." *Public Health Nutrition*. [Cambridge Core](https://www.cambridge.org/core/journals/public-health-nutrition)
- OR-Tools Linear Solver Example: Diet Problem. [Google Developers](https://developers.google.com/optimization/lp/glop)

### Difficulte : 2/5

---

## A3 - Ordonnancement de blocs operatoires

L'ordonnancement des blocs operatoires est un probleme de scheduling complexe ou il faut planifier des interventions chirurgicales dans des salles d'operation partagees, sous des contraintes de disponibilite des chirurgiens, des anesthesistes, des equipements specifiques, et des durees estimees variables. Le modele CP-SAT utilise des IntervalVar pour representer chaque intervention, des contraintes NoOverlap pour les salles, et des contraintes Cumulative pour le personnel. L'objectif est de minimiser le makespan tout en respectant les urgences, les preferences des equipes, et les temps de nettoyage entre interventions.

### Objectifs
- Modeliser le bloc operatoire comme un job-shop avec ressources cumulatives (chirurgiens, salles, equipements) via IntervalVar et Cumulative
- Implementer les contraintes de precedence (urgence avant elective), disponibilite du personnel, et temps de nettoyage
- Ajouter des soft constraints pour les preferences des chirurgiens et la minimisation des temps d'attente des patients
- Evaluer sur des instances de la litterature (Owstream benchmarks, donnees hospitalieres synthetiques)
- Comparer avec une approche par regles de priorite et une metaheuristique (simulated annealing)

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-4 Scheduling | [Search/Part2-CSP/CSP-4-Scheduling.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-4-Scheduling.ipynb) | IntervalVar, NoOverlap, Cumulative |
| CSP-7 Soft Constraints | [Search/Part2-CSP/CSP-7-Soft.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-7-Soft.ipynb) | Penalites, preferences |
| App-4 Job-Shop Scheduling | [Search/Applications/CSP/App-4-JobShopScheduling.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Applications/CSP/App-4-JobShopScheduling.ipynb) | Job-shop CP-SAT |
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Optimisation multi-objectif |

### References externes
- Cardoen, B., Demeulemeester, E., & Belien, J. (2010). "Operating Room Planning and Scheduling: A Literature Review." *European Journal of Operational Research*, 201(3), 921-932. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0377221709003070)
- Guerriero, F., & Guido, R. (2016). "Operational Research in the Management of the Operating Theatre: A Survey." *Health Care Management Science*, 19, 89-114. [Springer](https://link.springer.com/article/10.1007/s10729-014-9290-2)
- OR-Tools Scheduling Example. [Google Developers](https://developers.google.com/optimization/scheduling/job_shop)
- van Oostrum, J.M., et al. (2008). "Surgical Planning in Hospitals." *Health Systems*, 1(1), 35-50. [Tandfonline](https://www.tandfonline.com/doi/abs/10.1057/palgrave.hs.2006.2)

### Difficulte : 3/5

---

## A4 - Optimisation stochastique de protocoles pharmaceutiques

L'optimisation des protocoles de traitement pharmaceutique (en particulier en oncologie) consiste a determiner les dosages et calendriers d'administration de medicaments qui maximisent l'efficacite therapeutique tout en minimisant les effets secondaires toxiques. Ce probleme comporte une forte composante stochastique (variabilite inter-patient, incertitude sur la reponse) qui peut etre apprehendee par des modeles CP robustes ou stochastiques. La modelisation CP permet de capturer les contraintes de dose cumulative maximale, les intervalles minimum entre administrations, et les interactions medicamenteuses.

### Objectifs
- Modeliser un protocole de chimiotherapie comme un probleme de scheduling sous contraintes de dose, toxicite et intervalle avec CP-SAT
- Integrer l'incertitude sur la reponse patient via des scenarios stochastiques ou de l'optimisation robuste
- Implementer les contraintes pharmacocinetiques (demi-vie, concentration maximale, accumulation)
- Comparer les approches deterministe, robuste et stochastique sur des profils de patients synthetiques
- Visualiser les protocoles optimaux et les zones de risque (toxicite vs efficacite)

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-4 Scheduling | [Search/Part2-CSP/CSP-4-Scheduling.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-4-Scheduling.ipynb) | IntervalVar, contraintes temporelles |
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Optimisation sous contraintes |
| Search-11 Metaheuristiques | [Search/Part1-Foundations/Search-11-Metaheuristics.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-11-Metaheuristics.ipynb) | Optimisation stochastique |
| Probas/ (Infer.NET) | [Probas/](https://github.com/jsboige/CoursIA/tree/main/MyIA.AI.Notebooks/Probas) | Programmation probabiliste |

### References externes
- Agur, Z., et al. (2006). "Effect of Dosing Interval on Myelotoxicity and Survival in Computerized Controlled Clinical Trials of 1-beta-D-Arabinofuranosylcytosine." *Cell Proliferation*, 29(6), 359-374. [Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1365-2184.1996.tb00984.x)
- Fiandaca, G., et al. (2022). "Mathematical Models in Oncology: A Comprehensive Review." *Cancers*, 14(17), 4101. [MDPI](https://www.mdpi.com/2072-6694/14/17/4101)
- Bertsimas, D., et al. (2016). "Data-Driven Optimization in Cancer Treatment." *INFORMS Journal on Computing*. [INFORMS](https://pubsonline.informs.org/doi/10.1287/ijoc.2016.0687)
- OR-Tools CP-SAT Documentation: Interval Variables. [Google Developers](https://developers.google.com/optimization/cp/cp_solver#interval_variables)

### Difficulte : 4/5

---

## B1 - Equilibrage de chaine d'assemblage (SALBP)

Le Simple Assembly Line Balancing Problem (SALBP) consiste a repartir un ensemble de taches elementaires sur les stations d'une ligne d'assemblage, en respectant les contraintes de precedence entre taches et la cadence imposee (cycle time). L'objectif est de minimiser le nombre de stations (SALBP-1) ou le temps de cycle (SALBP-2). C'est un probleme classique de CP ou chaque tache est assignee a une station avec des contraintes de precedence et de temps cumule par station. Le modele CP-SAT est direct et performant, avec des applications industrielles dans l'automobile, l'electronique et l'agroalimentaire.

### Objectifs
- Modeliser le SALBP-1 (minimiser les stations) et SALBP-2 (minimiser le cycle time) en CP-SAT
- Implementer les contraintes de precedence, de temps de cycle, et d'exclusion mutuelle entre taches
- Etendre aux variantes multi-modeles (mixing plusieurs produits sur la meme ligne) et multi-objectifs
- Benchmarker sur les instances de la litterature (Otto et al., 2013) disponibles en ligne
- Comparer CP-SAT avec une heuristique de priorite (Ranked Positional Weight) et un modele PLNE

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-4 Scheduling | [Search/Part2-CSP/CSP-4-Scheduling.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-4-Scheduling.ipynb) | IntervalVar, NoOverlap, scheduling |
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Bin Packing, optimisation |
| App-4 Job-Shop Scheduling | [Search/Applications/CSP/App-4-JobShopScheduling.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Applications/CSP/App-4-JobShopScheduling.ipynb) | Job-shop, affectation de taches |
| Search-1 StateSpace | [Search/Part1-Foundations/Search-1-StateSpace.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-1-StateSpace.ipynb) | Graphes, parcours |

### References externes
- Scholl, A. (1999). "Balancing and Sequencing of Assembly Lines." *Physica-Verlag*. [Springer](https://link.springer.com/book/9783790811803)
- Otto, A., Otto, C., & Scholl, A. (2013). "Systematic Data Generation and Test Design for Computational Experiments with SALBP Instances." *European Journal of Operational Research*, 228(1), 33-45. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0377221713000757)
- SALBP Benchmark Instances (Assembly-Line-Balancing.de). [ALB](https://assembly-line-balancing.de/)
- Boysen, N., Fliedner, M., & Scholl, A. (2007). "A Classification of Assembly Line Balancing Problems." *European Journal of Operational Research*, 183(2), 674-693. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0377221707005739)

### Difficulte : 3/5

---

## B2 - Conception de chaine logistique (Supply Chain Network Design)

Le Supply Chain Network Design consiste a determiner l'emplacement optimal d'entrepots et de centres de distribution, les flux de marchandises entre fournisseurs, entrepots et clients, sous des contraintes de capacite, de demande, et de couts de transport. C'est un probleme de localisation-allocation qui se decompose en un probleme de p-median/p-center pour la localisation, et un probleme de flot pour l'allocation. La modelisation CP-SAT permet de capturer les contraintes discretes (ouvrir/fermer un entrepot), les capacites, et les choix multimodaux de transport.

### Objectifs
- Modeliser le Supply Chain Network Design comme un probleme de localisation-allocation avec CP-SAT
- Implementer les contraintes de capacite d'entrepots, demande client, et couts de transport variables
- Ajouter des contraintes de robustesse (demande incertaine) et de durabilite (emissions CO2, camions electriques)
- Evaluer sur des instances reelles (CAP - Capacitated Plant Location) et des benchmarks synthetiques
- Comparer avec une resolution PLNE et une metaheuristique (GRASP ou ALNS)

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Knapsack, Bin Packing, allocation |
| CSP-9 Distributed CSP | [Search/Part2-CSP/CSP-9-Distributed.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-9-Distributed.ipynb) | Multi-agent, supply chains |
| App-17 VRP Logistics | [Search/Applications/Hybrid/App-17-VRP-Logistics.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Applications/Hybrid/App-17-VRP-Logistics.ipynb) | VRP, logistique |
| Search-9 Programmation lineaire | [Search/Part1-Foundations/Search-9-LinearProgramming.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-9-LinearProgramming.ipynb) | PLNE, localisation |

### References externes
- Melo, M.T., Nickel, S., & Saldanha-da-Gama, F. (2009). "Facility Location and Supply Chain Management - A Literature Review." *European Journal of Operational Research*, 196(2), 401-412. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0377221708003614)
- Daskin, M.S. (2013). "Network and Discrete Location: Models, Algorithms, and Applications." *Wiley*. [Wiley](https://www.wiley.com/en-us/Network+and+Discrete+Location%3A+Models%2C+Algorithms%2C+and+Applications%2C+2nd+Edition-p-9780470905364)
- Beasley OR-Library: Capacitated Plant Location. [Brunel](http://people.brunel.ac.uk/~mastjjb/jeb/orlib/capinfo.html)
- Farahani, R.Z., et al. (2014). "Competitive Supply Chain Network Design: An Overview." *Computers & Operations Research*, 42, 328-346. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0305054813002105)

### Difficulte : 3/5

---

## B3 - Chargement de conteneurs (Bin Packing 3D)

Le Bin Packing 3D consiste a optimiser le chargement d'un ensemble d'objets parallelepipediques dans un nombre minimal de conteneurs (ou camions), en respectant les contraintes geometriques de non-chevauchement, d'orientation (certains objets ne peuvent etre tournes), de fragilite (ne pas poser d'objet lourd sur un objet fragile), et de stabilite (le centre de gravite doit rester dans une zone acceptable). C'est une extension 3D du Bin Packing classique, avec des contraintes geometriques qui rendent le modele CP-SAT riche et interessant.

### Objectifs
- Modeliser le Bin Packing 3D en CP-SAT avec des variables de position (x, y, z) et de dimension pour chaque objet
- Implementer les contraintes de non-chevauchement 3D, d'orientation, de fragilite et de stabilite
- Ajouter des contraintes de poids maximal par conteneur et de centre de gravite
- Benchmarker sur les instances de Martello et Vigo (2000) et les benchmarks PACKLIB
- Comparer avec des heuristiques de placement (Bottom-Left-Fill, Maximal Rectangles)

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Bin Packing, Knapsack |
| CSP-1 Fondamentaux | [Search/Part2-CSP/CSP-1-Fundamentals.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-1-Fundamentals.ipynb) | Modelisation CSP |
| App-10 Portfolio | [Search/Applications/Hybrid/App-10-Portfolio.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Applications/Hybrid/App-10-Portfolio.ipynb) | Optimisation combinatoire |
| Search-4 Local Search | [Search/Part1-Foundations/Search-4-LocalSearch.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-4-LocalSearch.ipynb) | Heuristiques locales |

### References externes
- Martello, S., Pisinger, D., & Vigo, D. (2000). "The Three-Dimensional Bin Packing Problem." *Operations Research*, 48(2), 256-267. [INFORMS](https://pubsonline.informs.org/doi/abs/10.1287/opre.48.2.256.12386)
- Crainic, T.G., Perboli, G., & Tadei, R. (2008). "Extreme Point-Based Heuristics for Three-Dimensional Bin Packing." *INFORMS Journal on Computing*, 20(3), 368-384. [INFORMS](https://pubsonline.informs.org/doi/10.1287/ijoc.1070.0248)
- PACKLIB: 3D Packing Benchmarks. [OR-Library](http://people.brunel.ac.uk/~mastjjb/jeb/orlib/binpackinfo.html)
- Zhao, X., et al. (2021). "A Survey on Three-Dimensional Container Loading." *European Journal of Operational Research*. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0377221721007165)

### Difficulte : 3/5

---

## B4 - Ordonnancement industriel (RCPSP)

Le Resource-Constrained Project Scheduling Problem (RCPSP) est le probleme de reference en ordonnancement sous contraintes de ressources. Il consiste a planifier un ensemble de taches avec des contraintes de precedence et des ressources renouvelables limitees (personnel, machines, budget) de maniere a minimiser le makespan. Le RCPSP generalise le job-shop scheduling et constitue le benchmark canonique en CP. Les modeles CP-SAT avec IntervalVar et Cumulative sont particulierement performants sur ce probleme, et les benchmarks PSPLIB fournissent des instances allant de 30 a 1200 taches.

### Objectifs
- Modeliser le RCPSP en CP-SAT avec IntervalVar (taches), NoOverlap (precedence) et Cumulative (ressources)
- Implementer les variantes RCPSP/max (decalages temporels generalises) et multi-mode (plusieurs durees/ressources par tache)
- Evaluer sur les instances PSPLIB (j30, j60, j120) et comparer avec les meilleurs resultats publies
- Etudier l'impact des strategies de branchement (VSIDS, activity-based) sur les performances
- Comparer CP-SAT avec une metaheuristique (GA ou SA) sur les grandes instances (j120+)

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-4 Scheduling | [Search/Part2-CSP/CSP-4-Scheduling.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-4-Scheduling.ipynb) | IntervalVar, NoOverlap, Cumulative |
| App-4 Job-Shop Scheduling | [Search/Applications/CSP/App-4-JobShopScheduling.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Applications/CSP/App-4-JobShopScheduling.ipynb) | Job-shop CP-SAT |
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Optimisation, objectifs multiples |
| Search-11 Metaheuristiques | [Search/Part1-Foundations/Search-11-Metaheuristics.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-11-Metaheuristics.ipynb) | GA, SA pour grands problemes |

### References externes
- Hartmann, S., & Briskorn, D. (2010). "A Survey of Variants and Extensions of the Resource-Constrained Project Scheduling Problem." *European Journal of Operational Research*, 207(1), 1-14. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0377221709017878)
- PSPLIB: Project Scheduling Problem Library. [PSPLIB](https://www.om-db.wi.tum.de/psplib/)
- Laborie, P. (2009). "IBM ILOG CP Optimizer for Detailed Scheduling Illustrated on Three Problems." *CPAIOR*. [Springer](https://link.springer.com/chapter/10.1007/978-3-642-01929-6_12)
- Ormann, W.P., et al. (2009). "A Survey of the State-of-the-Art in RCPSP." *International Journal of Production Research*. [Tandfonline](https://www.tandfonline.com/doi/abs/10.1080/00207540903165123)

### Difficulte : 3/5

---

## C1 - Tournees de livraison vertes (Electric VRP)

Le Electric Vehicle Routing Problem (EVRP) etend le Vehicle Routing Problem classique en ajoutant des contraintes d'autonomie de batterie, de recharge aux bornes, et de couts energetiques variables selon le profil de la route (pente, vitesse, charge transportee). L'objectif est de planifier les tournees d'une flotte de camions electriques en minimisant la distance totale ou les emissions de CO2, tout en respectant les fenetres horaires des clients et les capacites des vehicules. La modelisation CP-SAT combine des contraintes de tournees (Circuit), de capacite (Knapsack), et d'autonomie (fenetres cumulatives). **Note** : contrairement au VRP classique (EPF, annexe #20), l'EVRP introduit des contraintes de consommation energetique variable et de localisation de bornes de recharge qui modifient structurellement le modele CP-SAT (variables binaires de recharge, contraintes cumulatives non-lineaires de degradation batterie, decisions conjointes de tournees ET de placement de bornes).

### Objectifs
- Modeliser l'EVRP en CP-SAT avec contraintes de tournee, capacite, autonomie batterie et recharge
- Implementer les contraintes de consommation energetique variable (distance, charge, pente)
- Ajouter la localisation optimale des bornes de recharge comme variable de decision
- Evaluer sur les benchmarks EVRP de la litterature (Schneider et al., 2014; Felipe et al., 2014)
- Comparer CP-SAT avec ALNS (Adaptive Large Neighborhood Search) sur les grandes instances

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| App-17 VRP Logistics | [Search/Applications/Hybrid/App-17-VRP-Logistics.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Applications/Hybrid/App-17-VRP-Logistics.ipynb) | VRP CP-SAT, SA, GA, ACO |
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Knapsack, capacite |
| App-13 TSP Metaheuristics | [Search/Applications/Hybrid/App-13-TSP-Metaheuristics.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Applications/Hybrid/App-13-TSP-Metaheuristics.ipynb) | TSP, tournees |

### References externes
- Schneider, M., Stenger, A., & Goeke, D. (2014). "The Electric Vehicle-Routing Problem with Time Windows and Recharging Stations." *Transportation Science*, 48(4), 500-520. [INFORMS](https://pubsonline.informs.org/doi/abs/10.1287/trsc.2013.0490)
- Felipe, A., et al. (2014). "A Heuristic Approach for the Green Vehicle Routing Problem." *Expert Systems with Applications*, 41(14), 6424-6437. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0957417414002159)
- Erdelic, T., & Caric, T. (2019). "A Survey on the Electric Vehicle Routing Problem: Variants and Solution Approaches." *Journal of Advanced Transportation*. [Hindawi](https://www.hindawi.com/journals/jat/2019/5075671/)
- Xiao, Y., et al. (2012). "Development of a Fuel Consumption Optimization Model for the Capacitated Vehicle Routing Problem." *Computers & Operations Research*, 39(7), 1419-1431. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0305054811002731)

### Difficulte : 3/5

---

## C2 - Ordonnancement ferroviaire (Railway Timetabling)

Le Railway Timetabling Problem consiste a planifier les passages de trains sur un reseau ferroviaire en respectant les contraintes de voie unique (sur certains troncons), de signalisation (intervalles minimum entre trains), de correspondances (correspondance entre lignes), et de temps de trajet minimum/maximum. C'est un probleme de scheduling massif avec des ressources partagees (voies, quais, signaux) qui se modelise avec IntervalVar, NoOverlap (pour les troncons a voie unique) et Cumulative (pour les gares a quais multiples). Le modele PESP (Periodic Event Scheduling Problem) est la formalisation de reference. **Note** : contrairement au timetabling universitaire (annexe #14), le Railway Timetabling opere sur des ressources continues (trons de voie avec longueur et signalisation), des contraintes periodiques strictes (PESP), des blocs de voie exclusive (NoOverlap sur des intervalles temporels longs), et un reseau physique fixe avec des goulets d'etranglement. L'espace de solution est structurellement different : pas de "salles" discretes mais des "trons de voie" avec capacite 1 et temps de traversal variables selon le type de train.

### Objectifs
- Modeliser le Railway Timetabling comme un probleme PESP avec contraintes periodiques et CP-SAT
- Implementer les contraintes de bloc (voies uniques), de signalisation, et de correspondance entre lignes
- Ajouter la gestion des perturbations (retards) comme un probleme de re-scheduling en temps reel
- Evaluer sur les instances PESP et les benchmarks ferroviaires (ROSA, FPtransport)
- Analyser la scalabilite du modele CP-SAT sur des reseaux de taille reelle

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-4 Scheduling | [Search/Part2-CSP/CSP-4-Scheduling.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-4-Scheduling.ipynb) | IntervalVar, NoOverlap, Cumulative |
| App-4 Job-Shop Scheduling | [Search/Applications/CSP/App-4-JobShopScheduling.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Applications/CSP/App-4-JobShopScheduling.ipynb) | Job-shop, ressources partagees |
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Optimisation multi-objectif |
| Planners-7 OR-Tools | [SymbolicAI/Planners/03-Advanced/Planners-7-OR-Tools.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Planners/03-Advanced/Planners-7-OR-Tools.ipynb) | Planification temporelle avec IntervalVar |

### References externes
- Serafini, P., & Ukovich, W. (1989). "A Mathematical Model for Periodic Scheduling Problems." *SIAM Journal on Discrete Mathematics*, 2(4), 550-581. [SIAM](https://epubs.siam.org/doi/abs/10.1137/0402049)
- Lusby, R.M., et al. (2011). "Railway Track Allocation: Models and Methods." *OR Spectrum*, 33(4), 843-883. [Springer](https://link.springer.com/article/10.1007/s00291-009-0188-0)
- Cacchiani, V., et al. (2014). "An Overview of Recovery Models and Algorithms for Real-Time Railway Rescheduling." *Transportation Research Part B*, 63, 15-37. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0191261514000226)
- Kroon, L., et al. (2009). "The New Dutch Timetable: The OR Revolution." *Interfaces*, 39(1), 6-17. [INFORMS](https://pubsonline.informs.org/doi/abs/10.1287/inte.1080.0402)

### Difficulte : 4/5

---

## C3 - Livraison par drones (Drone Delivery Routing)

Le Drone Delivery Routing Problem consiste a planifier les tournees d'une flotte de drones de livraison depuis un depot central, en respectant les contraintes d'autonomie (batterie), de capacite de charge (poids et volume), de zones de vol interdites, et de conditions meteorologiques. Ce probleme est une variante du VRP avec des specificites aeriennes : les drones ne sont pas soumis aux contraintes routieres mais ont une autonomie limitee et une capacite reduite. Le modele CP-SAT combine des contraintes de tournees, de capacite knapsack, et d'autonomie cumulative avec rechargement au depot. **Note** : contrairement au VRP classique (annexe #20), le Drone VRP opere en espace euclidien 3D (pas de graphe routier), avec des contraintes de zone de vol interdite (polygones NOTAM), de distance euclidienne au lieu de plus court chemin routier, et de conditions meteorologiques dynamiques qui modifient l'autonomie en vol. Le graphe de tournees est fondamentalement different (complete, pondere par distance euclidienne vs sparse, pondere par reseau routier).

### Objectifs
- Modeliser le Drone Delivery Routing comme un VRP avec contraintes specifiques drones (autonomie, capacite, zones) en CP-SAT
- Implementer les contraintes de zone de vol interdite (polygones) et de distance euclidienne
- Ajouter la coordination multi-drone (collision avoidance, synchronisation au depot)
- Evaluer sur des instances synthetiques basees sur des donnees urbaines reelles
- Comparer avec un modele de tournnees camions (classical VRP) pour quantifier l'apport drones

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| App-17 VRP Logistics | [Search/Applications/Hybrid/App-17-VRP-Logistics.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Applications/Hybrid/App-17-VRP-Logistics.ipynb) | VRP CP-SAT |
| CSP-4 Scheduling | [Search/Part2-CSP/CSP-4-Scheduling.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-4-Scheduling.ipynb) | Scheduling, ressources |
| App-13 TSP Metaheuristics | [Search/Applications/Hybrid/App-13-TSP-Metaheuristics.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Applications/Hybrid/App-13-TSP-Metaheuristics.ipynb) | TSP, heuristiques |
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Optimisation combinatoire |

### References externes
- Murray, C.C., & Chu, A.G. (2015). "The Flying Sidekick Traveling Salesman Problem: Optimization of Drone-Assisted Parcel Delivery." *Transportation Research Part C*, 54, 86-109. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0968090X15001333)
- Poikonen, S., et al. (2017). "Vehicle Routing Problems with Drones: Extended Models and Algorithms." *European Journal of Operational Research*. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0377221719304651)
- Otto, A., et al. (2018). "Optimization of a Multi-Drone Delivery Network." *Transportation Research Part C*. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0968090X18301013)
- Dorling, K., et al. (2017). "Vehicle Routing Problems for Drone Delivery." *IEEE Transactions on Systems, Man, and Cybernetics*. [IEEE](https://ieeexplore.ieee.org/document/7493220)

### Difficulte : 3/5

---

## C4 - Assemblage orbital de satellites (Orbital Assembly Scheduling)

L'assemblage orbital de satellites consiste a planifier les manoeuvres de rendez-vous spatial entre modules autonomes (propulsion, charge utile, panneaux solaires) qui doivent s'assembler en orbite pour former un satellite complet. Contrairement au scheduling d'observations (traité par EPITA 2025), ce sujet se concentre sur la planification de manoeuvres orbitales (changements d'orbite, synchronisation de vitesses, approche finale) avec des contraintes de carburant (delta-V limite par manoeuvre), de fenetres de lancement, de communication avec le sol, et de secuence d'assemblage (certains modules doivent etre installes avant d'autres). C'est un probleme de scheduling spatial structurellement different de la planification d'observations.

### Objectifs
- Modeliser l'assemblage orbital en CP-SAT avec IntervalVar pour les manoeuvres et NoOverlap pour les exclusions mutuelles orbitales
- Implementer les contraintes de delta-V (budget carburant cumulatif), de fenetres de lancement, et de precedence entre modules
- Ajouter les contraintes de communication (visibilite stations sol) et de securite (distance minimale entre modules)
- Evaluer sur des instances synthetiques basees sur les parametres orbitaux reels (LEO, GEO, transfert de Hohmann)
- Comparer CP-SAT avec un ordonnancement glouton par fenetres de lancement priorisees

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-4 Scheduling | [Search/Part2-CSP/CSP-4-Scheduling.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-4-Scheduling.ipynb) | IntervalVar, NoOverlap, Cumulative |
| App-4 Job-Shop Scheduling | [Search/Applications/CSP/App-4-JobShopScheduling.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Applications/CSP/App-4-JobShopScheduling.ipynb) | Precedences, makespan |
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Optimisation sous contraintes |
| Search-11 Metaheuristiques | [Search/Part1-Foundations/Search-11-Metaheuristics.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-11-Metaheuristics.ipynb) | Metaheuristiques |

### References externes
- Flury, W. (1992). "Rendezvous in Space." *Acta Astronautica*, 27, 195-205. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/009457659290075P)
- Fehse, W. (2003). *Automated Rendezvous and Docking of Spacecraft*. Cambridge University Press. [Cambridge](https://www.cambridge.org/core/books/automated-rendezvous-and-docking-of-spacecraft/)
- Goodman, J.L. (2009). "History of Space Shuttle Rendezvous and Proximity Operations." *Journal of Spacecraft and Rockets*. [AIAA](https://arc.aiaa.org/doi/abs/10.2514/1.34396)
- Izzo, D. (2015). "PyGMO and PyKEP: Open Source Tools for Massively Parallel Optimization in Astrodynamics." *5th International Conference on Astrodynamics Tools and Techniques*. [ESA](https://www.esa.int/gsp/ACT/projects/pygmo_pykep)

### Difficulte : 4/5

---

## D1 - Allocation de ressources cloud (VM Scheduling)

Le VM Scheduling Problem consiste a allouer des machines virtuelles (VMs) avec des caracteristiques heterogenes (CPU, RAM, stockage, bande passante) sur des serveurs physiques, sous des contraintes de capacite, d'affinite (certaines VMs doivent etre co-localisees ou separees pour des raisons de securite/performance), et de resilience (anti-affinite pour la tolerance aux pannes). C'est un probleme de Bin Packing multi-dimensionnel avec des contraintes d'affinite, directement modelisable en CP-SAT.

### Objectifs
- Modeliser le VM Scheduling comme un Bin Packing multi-dimensionnel avec contraintes d'affinite en CP-SAT
- Implementer les contraintes de capacite (CPU, RAM, stockage), d'affinite/anti-affinite, et de resilience
- Ajouter la consolidation dynamique (migration de VMs) et la minimisation de la fragmentation
- Evaluer sur des instances reelles (Google Cluster Trace) et des benchmarks synthetiques
- Comparer avec le First Fit Decreasing (FFD) et un modele PLNE sur les memes instances

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Bin Packing, Knapsack |
| CSP-1 Fondamentaux | [Search/Part2-CSP/CSP-1-Fundamentals.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-1-Fundamentals.ipynb) | Modelisation CSP |
| Search-9 Programmation lineaire | [Search/Part1-Foundations/Search-9-LinearProgramming.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-9-LinearProgramming.ipynb) | PLNE, relaxation |
| CSP-7 Soft Constraints | [Search/Part2-CSP/CSP-7-Soft.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-7-Soft.ipynb) | Preferences, penalites |

### References externes
- Mann, Z.A. (2015). "Allocation of Virtual Machines in Cloud Data Centers - A Survey." *European Journal of Operational Research*, 246(3), 779-798. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0377221715003633)
- Google Cluster Trace. [GitHub](https://github.com/google/cluster-data)
- Beloglazov, A., & Buyya, R. (2012). "Optimal Online Deterministic Algorithms and Adaptive Heuristics for Energy and Performance Efficient Dynamic Consolidation." *Future Generation Computer Systems*, 28(5), 753-768. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0167739X11000689)
- Salimian, A., et al. (2017). "A Survey of Energy-Aware Scheduling in Cloud Computing." *The Journal of Supercomputing*. [Springer](https://link.springer.com/article/10.1007/s11227-017-2190-3)

### Difficulte : 3/5

---

## D2 - Optimisation energetique de centres de donnees

L'optimisation energetique des centres de donnees consiste a minimiser la consommation electrique (PUE - Power Usage Effectiveness) en reglant dynamiquement l'etat des serveurs (actif, veille, eteint), la consolidation des charges de travail, et l'utilisation du free cooling (refroidissement par air exterieur). Les contraintes portent sur la capacite de traitement, la temperature maximale des salles, les SLA (Service Level Agreements), et la disponibilite de l'energie renouvelable. C'est un probleme d'ordonnancement sous contraintes de ressources et d'energie, pionnier chez Google.

### Objectifs
- Modeliser l'ordonnancement energetique comme un probleme de consolidation dynamique avec CP-SAT
- Implementer les contraintes de temperature, de SLA, de capacite de refroidissement et d'energie renouvelable
- Ajouter la gestion des cretes de consommation (peak shaving) par ordonnancement differe
- Evaluer sur des profils de charge reels (Google Cluster Trace, Azure Trace) et des donnees meteorologiques
- Comparer l'approche CP-SAT avec une politique de seuil (hysteresis) et une metaheuristique

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-4 Scheduling | [Search/Part2-CSP/CSP-4-Scheduling.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-4-Scheduling.ipynb) | IntervalVar, scheduling |
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Bin Packing, consolidation |
| CSP-7 Soft Constraints | [Search/Part2-CSP/CSP-7-Soft.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-7-Soft.ipynb) | Soft constraints, compromis |
| Search-11 Metaheuristiques | [Search/Part1-Foundations/Search-11-Metaheuristics.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-11-Metaheuristics.ipynb) | Optimisation globale |

### References externes
- Beloglazov, A., et al. (2012). "Energy-Aware Resource Allocation Heuristics for Efficient Management of Data Centers." *Future Generation Computer Systems*, 28(5), 755-768. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0167739X11000689)
- Google Environmental Report: Data Centers. [Google](https://environment.google/responsible-supply-chain/data-centers/)
- Orgerie, A.C., et al. (2014). "A Survey on Techniques for Improving the Energy Efficiency of Large-Scale Distributed Systems." *ACM Computing Surveys*, 46(4). [ACM DL](https://dl.acm.org/doi/10.1145/2532368)
- Dayarathna, M., et al. (2016). "Data Center Energy Consumption Modeling: A Survey." *IEEE Communications Surveys & Tutorials*, 18(1), 732-794. [IEEE](https://ieeexplore.ieee.org/document/7186553)

### Difficulte : 3/5

---

## D3 - Placement de services en edge computing

Le placement de services en edge computing consiste a determiner sur quels noeuds de bord de reseau (edge nodes) deployer des microservices (ou des fonctions serverless) de maniere a minimiser la latence percue par les utilisateurs, sous des contraintes de capacite de calcul, de memoire, de bande passante, et de couverture geographique. C'est un probleme de localisation-allocation avec des contraintes de latence (SLA temporel), directement apparente au p-median avec contraintes de capacite. La modelisation CP-SAT est naturelle avec des variables binaires d'affectation et des contraintes de distance maximale.

### Objectifs
- Modeliser le placement de services edge comme un probleme de localisation-allocation avec CP-SAT
- Implementer les contraintes de latence (distance reseau), de capacite (CPU, RAM, bande passante), et de redondance
- Ajouter la dynamique temporelle (variation de charge au cours de la journee) avec un modele multi-periodes
- Evaluer sur des topologies reelles (Azure Edge, AWS Wavelength) et des traces de charge synthetiques
- Comparer avec un algorithme glouton (nearest fit) et un modele PLNE relaxe

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Allocation, Knapsack |
| CSP-1 Fondamentaux | [Search/Part2-CSP/CSP-1-Fundamentals.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-1-Fundamentals.ipynb) | Modelisation CSP |
| Search-1 StateSpace | [Search/Part1-Foundations/Search-1-StateSpace.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-1-StateSpace.ipynb) | Graphes, parcours |
| CSP-9 Distributed CSP | [Search/Part2-CSP/CSP-9-Distributed.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-9-Distributed.ipynb) | Multi-agent, distribution |

### References externes
- Mao, Y., et al. (2017). "A Survey on Mobile Edge Computing: The Communication Perspective." *IEEE Communications Surveys & Tutorials*, 19(4), 2322-2358. [IEEE](https://ieeexplore.ieee.org/document/7932343)
- Lai, P., et al. (2020). "Optimal Edge Service Placement in Mobile Edge Computing." *IEEE Transactions on Mobile Computing*. [IEEE](https://ieeexplore.ieee.org/document/8920320)
- Wang, X., et al. (2019). "Convergence of Edge Computing and Deep Learning." *IEEE Wireless Communications*. [IEEE](https://ieeexplore.ieee.org/document/8732352)
- Mach, P., & Becvar, Z. (2017). "Mobile Edge Computing: A Survey on Architecture and Computation Offloading." *IEEE Communications Surveys & Tutorials*, 19(3), 1628-1656. [IEEE](https://ieeexplore.ieee.org/document/7899390)

### Difficulte : 3/5

---

## D4 - Dispatch dans un reseau electrique

Le dispatch economique (Economic Dispatch) consiste a determiner la production optimale de chaque centrale electrique d'un reseau pour satisfaire la demande a chaque instant, en minimisant le cout total de production tout en respectant les contraintes de capacite des lignes de transport, les limites de generation par centrale, et l'equilibre offre-demande en temps reel. Avec l'integration des energies renouvelables intermittentes (eolien, solaire), le probleme devient stochastique. La modelisation CP-SAT capture les contraintes discretes (on/off des centrales, demarrage minimum) et les contraintes lineaires de flux.

### Objectifs
- Modeliser le dispatch economique comme un probleme d'optimisation sous contraintes avec CP-SAT
- Implementer les contraintes de capacite de generation, de lignes de transport, et d'equilibre offre-demande
- Ajouter les couts de demarrage/arret des centrales (unit commitment) et les reserves de spinning
- Etendre au cas stochastique avec des scenarios de production renouvelable (eolien, solaire)
- Evaluer sur des instances IEEE (IEEE 14-bus, 30-bus, 118-bus) et des donnees RTE France

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| Search-9 Programmation lineaire | [Search/Part1-Foundations/Search-9-LinearProgramming.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-9-LinearProgramming.ipynb) | PLNE, simplex, optimisation lineaire |
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Optimisation sous contraintes |
| CSP-4 Scheduling | [Search/Part2-CSP/CSP-4-Scheduling.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-4-Scheduling.ipynb) | IntervalVar, scheduling temporel |
| App-10 Portfolio | [Search/Applications/Hybrid/App-10-Portfolio.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Applications/Hybrid/App-10-Portfolio.ipynb) | Optimisation sous contraintes de budget |

### References externes
- Wood, A.J., & Wollenberg, B.F. (2012). "Power Generation, Operation, and Control." *Wiley*. [Wiley](https://www.wiley.com/en-us/Power+Generation%2C+Operation%2C+and+Control%2C+3rd+Edition-p-9780471790556)
- Padhy, N.P. (2004). "Unit Commitment - A Bibliographical Survey." *IEEE Transactions on Power Systems*, 19(2), 1196-1205. [IEEE](https://ieeexplore.ieee.org/document/1291440)
- IEEE Power Systems Test Case Archive. [University of Washington](https://labs.ece.uw.edu/pstca/)
- RTE France - Donnees en energie. [RTE](https://www.services-rte.com/fr/visualisez-les-donnees-publiees-par-rte.html)

### Difficulte : 4/5

---

## E1 - Super-optimisation gas Solidity par Max-SMT

La super-optimisation de smart contracts Ethereum consiste a trouver automatiquement la sequence d'instructions EVM (Ethereum Virtual Machine) equivalente a un programme Solidite donnee, mais minimisant le cout en gas. Ce probleme se modelise comme un probleme de synthese de programmes sous contraintes d'equivalence fonctionnelle, ou les contraintes sont exprimees en SMT (Satisfiability Modulo Theories). L'outil Souffle ou Z3 permet de verifier l'equivalence entre le programme original et la version optimisee, tandis que l'objectif de minimisation du gas est un probleme d'optimisation Max-SMT.

### Objectifs
- Modeliser la super-optimisation EVM comme un probleme Max-SMT avec contraintes d'equivalence et objectif de gas minimum
- Implementer la verification d'equivalence fonctionnelle entre sequences d'instructions avec Z3
- Explorer l'espace des sequences d'instructions equivalentes via echantillonnage et contraintes SMT
- Evaluer sur des snippets Solidity courants (arithmetic operations, storage access, loops)
- Comparer avec les optimiseurs existants (solc --optimize, EOSii)

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| SC-14 Formal Verification | [SymbolicAI/SmartContracts/03-Foundry-Testing/SC-14-Formal-Verification.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/SmartContracts/03-Foundry-Testing/SC-14-Formal-Verification.ipynb) | Verification formelle Solidity |
| Linq2Z3 | [SymbolicAI/Linq2Z3.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Linq2Z3.ipynb) | Z3 SMT Solver |
| SC-13 Fuzz Testing | [SymbolicAI/SmartContracts/03-Foundry-Testing/SC-13-Fuzz-Invariants.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/SmartContracts/03-Foundry-Testing/SC-13-Fuzz-Invariants.ipynb) | Tests et verification |
| SC-7 Solidity Advanced | [SymbolicAI/SmartContracts/02-Solidity-Advanced/SC-7-Token-Standards.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/SmartContracts/02-Solidity-Advanced/SC-7-Token-Standards.ipynb) | EVM, gas, opcodes |

### References externes
- Permenev, A., et al. (2020). "VerX: Safety Verification of Smart Contracts." *IEEE S&P*. [IEEE](https://doi.org/10.1109/SP40000.2020.00024)
- So, S., & Oh, H. (2021). "SmarTest: Effectively Hunting Vulnerable Transaction Sequences in Smart Contracts through Call Sequence and Message Feedback." *USENIX Security*. [USENIX](https://www.usenix.org/conference/usenixsecurity21/presentation/so)
- Z3 SMT Solver. [GitHub](https://github.com/Z3Prover/z3)
- Ethereum Yellow Paper: Gas Schedule. [Ethereum](https://ethereum.github.io/yellowpaper/paper.pdf)
- **[ATTENTION: Reference suspecte]** Chow, S., et al. (2023). "Automated Smart Contract Optimization Using SMT." *arXiv*. [arXiv](https://arxiv.org/abs/2304.09638) -- Ce papier n'a pas pu etre verifie. L'URL arXiv et le titre pourraient etre incorrects ou fabriques. Verification manuelle requise.

### Difficulte : 4/5

---

## E2 - Ordonnancement MEV-resistant de transactions

L'ordonnancement des transactions dans un bloc blockchain est un probleme d'optimisation combinatoire : parmi les transactions en attente (mempool), selectionner et ordonner un sous-ensemble qui maximise les frais collectes par le validateur, sous les contraintes de taille de bloc, de dependances entre transactions (nonce), et de protection contre le MEV (Maximal Extractable Value). Ce probleme combine le Knapsack (selection) et le TSP (ordonnancement) avec des contraintes de precedences specifiques a la blockchain.

### Objectifs
- Modeliser la selection et l'ordonnancement de transactions comme un probleme CP-SAT (Knapsack + precedences)
- Implementer les contraintes de taille de bloc, de nonce (ordre des transactions par adresse), et de gas limit
- Ajouter des mecanismes anti-MEV (randomisation partielle, encryption, commit-reveal)
- Evaluer sur des donnees de mempool Ethereum (MEV-Geth logs, Flashbots auctions)
- Comparer les strategies greediest-fee, CP-SAT optimale, et MEV-Boost

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| SC-7 Solidity Advanced | [SymbolicAI/SmartContracts/02-Solidity-Advanced/SC-7-Token-Standards.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/SmartContracts/02-Solidity-Advanced/SC-7-Token-Standards.ipynb) | Gas, transactions |
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Knapsack, selection |
| GameTheory/ | [GameTheory/](https://github.com/jsboige/CoursIA/tree/main/MyIA.AI.Notebooks/GameTheory) | Encheres, strategies |
| CSP-4 Scheduling | [Search/Part2-CSP/CSP-4-Scheduling.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-4-Scheduling.ipynb) | Ordonnancement |

### References externes
- Daian, P., et al. (2020). "Flash Boys 2.0: Frontrunning in Decentralized Exchanges, Miner Extractable Value, and Consensus Instability." *IEEE S&P*. [IEEE](https://ieeexplore.ieee.org/document/9152675)
- Flashbots Research. [writings.flashbots.net](https://writings.flashbots.net/)
- Ethereum Mempool Architecture. [ethereum.org](https://ethereum.org/en/developers/docs/transactions/)
- Quintus, M., et al. (2022). "Fair Sequencing in Blockchain: MEV Resistance." *AFT'22*. [ACM](https://dl.acm.org/doi/10.1145/3559500)

### Difficulte : 3/5

---

## E3 - Synthese de circuits Zero-Knowledge sous contraintes

La synthese de circuits Zero-Knowledge (ZK circuits) consiste a compiler un programme (ou une assertion mathematique) en un circuit arithmetique (R1CS - Rank-1 Constraint System) qui peut etre prouve en zero-knowledge. Le defi est de minimiser le nombre de contraintes (qui determine le temps de preuve et la taille de la preuve) tout en preservant la correction fonctionnelle. Ce probleme d'optimisation se modelise naturellement en CP/SMT : chaque porte du circuit est une contrainte, et l'objectif est de minimiser le nombre de contraintes.

### Objectifs
- Modeliser la synthese de circuits ZK comme un probleme d'optimisation sous contraintes d'equivalence avec CP-SAT
- Implementer la generation de contraintes R1CS a partir d'une representation intermediaire
- Optimiser le nombre de contraintes par elimination de sous-expressions communes et selection d'operations
- Evaluer sur des primitives cryptographiques (hash functions, signatures) et des circuits courants
- Comparer avec les compilateurs existants (Circom, Noir, Halo2)

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| SC-15 Cryptography ZKP | [SymbolicAI/SmartContracts/04-Privacy-Cryptography/SC-15-Zero-Knowledge-Proofs.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/SmartContracts/04-Privacy-Cryptography/SC-15-Zero-Knowledge-Proofs.ipynb) | Zero-Knowledge Proofs |
| SC-16 Homomorphic Encryption | [SymbolicAI/SmartContracts/04-Privacy-Cryptography/SC-16-Homomorphic-Encryption.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/SmartContracts/04-Privacy-Cryptography/SC-16-Homomorphic-Encryption.ipynb) | Cryptographie avancee |
| Linq2Z3 | [SymbolicAI/Linq2Z3.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Linq2Z3.ipynb) | SMT solving |
| CSP-1 Fondamentaux | [Search/Part2-CSP/CSP-1-Fundamentals.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-1-Fundamentals.ipynb) | Modelisation CSP |

### References externes
- Ben-Sasson, E., et al. (2018). "Scalable, Transparent, and Post-Quantum Secure Computational Integrity." *IACR Cryptology ePrint Archive*. [ePrint](https://eprint.iacr.org/2018/046)
- Circom Language Documentation. [iden3.io](https://docs.circom.io/)
- Gabizon, A., et al. (2019). "PLONK: Permutations over Lagrange-Bases for Oecumenical Noninteractive Arguments of Knowledge." *ePrint*. [ePrint](https://eprint.iacr.org/2019/953)
- Thaler, J. (2022). "Proofs, Arguments, and Zero-Knowledge." *Foundations and Trends in Privacy and Security*. [Justin Thaler](https://people.cs.georgetown.edu/jthaler/ProofsArgsAndZK.html)

### Difficulte : 4/5

---

## E4 - Allocation de validators PoS par bin-packing

Dans un blockchain Proof-of-Stake (comme Ethereum 2.0), les validateurs sont affectes a des comites pour attester les blocs. L'affectation doit etre equitable (chaque validateur participe a un nombre similaire de comites), doit respecter les contraintes de taille de comite, et doit optimiser la distribution des validateurs appartenant au meme operateur (pour la resistance aux pannes et la decentralisation). Ce probleme se modelise comme un Bin Packing avec des contraintes d'equilibre et d'anti-affinite.

### Objectifs
- Modeliser l'affectation de validateurs comme un Bin Packing avec contraintes d'equilibre et d'anti-affinite en CP-SAT
- Implementer les contraintes de taille de comite, d'equilibre (variance minimale), et de separation des operateurs
- Ajouter la dynamique temporelle (les comites changent periodiquement, les validateurs entrent/sortent)
- Evaluer sur des donnees Ethereum Beacon Chain (validateurs reels, operateurs connus)
- Comparer avec l'algorithme actuel d'Ethereum (random shuffled) et un modele PLNE

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Bin Packing, allocation |
| SC-0 Blockchain Foundations | [SymbolicAI/SmartContracts/00-Foundations/SC-0-Cypherpunk-Origins.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/SmartContracts/00-Foundations/SC-0-Cypherpunk-Origins.ipynb) | Blockchain, consensus |
| GameTheory/ | [GameTheory/](https://github.com/jsboige/CoursIA/tree/main/MyIA.AI.Notebooks/GameTheory) | Coalitions, equilibre |
| CSP-7 Soft Constraints | [Search/Part2-CSP/CSP-7-Soft.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-7-Soft.ipynb) | Equilibre, penalites |

### References externes
- Buterin, V., & Griffith, V. (2017). "Casper the Friendly Finality Gadget." *arXiv*. [arXiv](https://arxiv.org/abs/1710.09437)
- Ethereum 2.0 Specifications: Committee Assignment. [GitHub](https://github.com/ethereum/consensus-specs)
- Dinh, T.T.A., et al. (2018). "Untangling Blockchain: A Data Processing View of Blockchain Systems." *IEEE TKDE*. [IEEE](https://ieeexplore.ieee.org/document/8293535)
- Fernandez-Carames, T.M., & Fraga-Lamas, P. (2020). "Towards Post-Quantum Blockchain." *IEEE Access*. [IEEE](https://ieeexplore.ieee.org/document/9043748)

### Difficulte : 3/5

---

## E5 - Verification formelle SMT de vulnerabilites Solidity

La verification formelle des smart contracts consiste a prouver mathematiquement l'absence de vulnerabilites (reentrancy, overflow, access control) en modelisant le contrat comme un systeme de transitions et en verifiant des proprietes de surete (safety) avec un solveur SMT (Z3). Contrairement au fuzz testing qui ne trouve que des bugs, la verification formelle garantit l'absence de classes entieres de vulnerabilites. Le probleme de verification se reduit a la satisfiabilite de formules logiques sur les etats du contrat.

### Objectifs
- Modeliser un smart contract Solidity comme un systeme de transitions avec etats et variables SMT
- Implementer la verification de proprietes de surete (no reentrancy, no overflow, access control) avec Z3
- Generer des contre-exemples (witnesses) quand une propriete est violee
- Evaluer sur des contrats vulnerables connus (SWC Registry, Damn Vulnerable DeFi)
- Comparer avec les outils existants (Mythril, Slither, Certora)

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| SC-14 Formal Verification | [SymbolicAI/SmartContracts/03-Foundry-Testing/SC-14-Formal-Verification.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/SmartContracts/03-Foundry-Testing/SC-14-Formal-Verification.ipynb) | Verification formelle |
| SC-13 Fuzz Testing | [SymbolicAI/SmartContracts/03-Foundry-Testing/SC-13-Fuzz-Invariants.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/SmartContracts/03-Foundry-Testing/SC-13-Fuzz-Invariants.ipynb) | Tests, proprietes |
| Linq2Z3 | [SymbolicAI/Linq2Z3.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Linq2Z3.ipynb) | Z3 SMT Solver |
| SC-7 Solidity Advanced | [SymbolicAI/SmartContracts/02-Solidity-Advanced/SC-7-Token-Standards.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/SmartContracts/02-Solidity-Advanced/SC-7-Token-Standards.ipynb) | Vulnerabilites, securite |

### References externes
- Feist, J., et al. (2019). "Slither: A Static Analysis Framework for Smart Contracts." *IEEE/WIC/ACM WI*. [GitHub](https://github.com/crytic/slither)
- SWC Registry: Smart Contract Weakness Classification. [swcregistry.io](https://swcregistry.io/)
- Alt, L., & Reitwiessner, C. (2018). "SMT-Based Verification of Solidity Smart Contracts." *ISoLA*. [Springer](https://link.springer.com/chapter/10.1007/978-3-030-03421-4_11)
- Permenev, A., et al. (2020). "VerX: Safety Verification of Smart Contracts." *IEEE S&P*. [IEEE](https://ieeexplore.ieee.org/document/9152646)

### Difficulte : 3/5

---

## F1 - Model checking hardware par SAT (IC3/PDR)

Le model checking materiel consiste a verifier formellement qu'un circuit numerique (processeur, controleur, bus) satisfait une propriete de correction (absence de deadlock, respect du protocole, equivalence avec la specification). L'algorithme IC3/PDR (Property Directed Reachability) est la methode de reference qui utilise un solveur SAT incremental pour explorer l'espace d'etats du circuit de maniere inverse, sans le construire explicitement. C'est un sujet au carrefour de la verification formelle et du SAT solving.

### Objectifs
- Comprendre et implementer l'algorithme IC3/PDR pour la verification de proprietes de surete sur des circuits digitaux
- Modeliser un circuit comme un systeme de transitions avec variables booleennes et contraintes SAT
- Implementer la generation de clauses d'induction et le raffinement iteratif
- Evaluer sur des circuits de la competition HWMCC (Hardware Model Checking Competition)
- Comparer avec un model checking BDD-base et l'outil ABC (Berkeley)

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| Linq2Z3 | [SymbolicAI/Linq2Z3.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Linq2Z3.ipynb) | Z3, SAT/SMT solving |
| CSP-1 Fondamentaux | [Search/Part2-CSP/CSP-1-Fundamentals.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-1-Fundamentals.ipynb) | Modelisation par contraintes |
| CSP-6 Hybridation CP+SAT | [Search/Part2-CSP/CSP-6-Hybridization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-6-Hybridization.ipynb) | SAT encoding, hybridation |
| Search-3 A* | [Search/Part1-Foundations/Search-3-Informed.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-3-Informed.ipynb) | Exploration d'espaces d'etats |

### References externes
- Bradley, A.R. (2011). "SAT-Based Model Checking without Unrolling." *VMCAI*. [Springer](https://doi.org/10.1007/978-3-642-18275-4_7)
- Een, N., et al. (2011). "Efficient Implementation of Property Directed Reachability." *FMCAD*. [IEEE](https://ieeexplore.ieee.org/document/6083135)
- HWMCC: Hardware Model Checking Competition. [fmv.jku.at](https://fmv.jku.at/hwmcc/)
- Biere, A., et al. (2021). "Handbook of Satisfiability." *IOS Press*, 2nd Edition. [IOS Press](https://iospress.nl/book/handbook-of-satisfiability-2/)
- ABC: A System for Sequential Synthesis and Verification. [Berkeley](https://people.eecs.berkeley.edu/~alanmi/abc/)

### Difficulte : 4/5

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

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| Linq2Z3 | [SymbolicAI/Linq2Z3.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Linq2Z3.ipynb) | SAT/SMT solving |
| CSP-1 Fondamentaux | [Search/Part2-CSP/CSP-1-Fundamentals.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-1-Fundamentals.ipynb) | Modelisation CSP |
| CSP-6 Hybridation CP+SAT | [Search/Part2-CSP/CSP-6-Hybridization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-6-Hybridization.ipynb) | SAT encoding |
| SC-15 Cryptography ZKP | [SymbolicAI/SmartContracts/04-Privacy-Cryptography/SC-15-Zero-Knowledge-Proofs.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/SmartContracts/04-Privacy-Cryptography/SC-15-Zero-Knowledge-Proofs.ipynb) | Cryptographie |

### References externes
- Biere, A. (2021). "CaDiCaL, Kissat MAB and Mate at the SAT Competition 2021." *SAT Competition*. [dblp](https://dblp.org/rec/conf/sat/BiereF21)
- Mouha, N., & Preneel, B. (2013). "Towards Finding Optimal Differential Characteristics for ARX." *FSE*. [IACR](https://eprint.iacr.org/2013/328)
- Sun, S., et al. (2013). "Automatic Security Evaluation and (Related-Key) Differential Characteristic Search: Application to SIMON, PRESENT, LBlock, DES(L) and Other Bit-Oriented Block Ciphers." *ASIACRYPT*. [IACR](https://eprint.iacr.org/2013/676)
- Bogdanov, A., et al. (2007). "PRESENT: An Ultra-Lightweight Block Cipher." *CHES*. [Springer](https://doi.org/10.1007/978-3-540-74735-2_31)

### Difficulte : 4/5

---

## F3 - Bounded Model Checking de programmes C

Le Bounded Model Checking (BMC) consiste a verifier qu'un programme C ne viole pas certaines proprietes (absence de debordement de tampon, dereferencement de pointeur null, division par zero) en depliant le programme sur un nombre fini d'etapes (bound) et en encodant les executions possibles comme des formules SAT/SMT. Si le solveur trouve une affectation satisfaisant la negation de la propriete, un contre-exemple (chemin menant au bug) est produit. C'est la technique utilisee par CBMC et ESBMC.

### Objectifs
- Implementer un BMC simplifie pour un sous-ensemble de C (affectations, conditions, boucles bornees) encodant les executions en SMT (Z3)
- Gerer les types de base (int, bool, tableaux) et les operations arithmetiques avec debordement
- Produire des contre-exemples concrets (valeurs d'entree menant au bug) quand une propriete est violee
- Evaluer sur des programmes C avec des bugs connus (benchmarks SV-COMP)
- Comparer avec CBMC sur les memes instances

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| Linq2Z3 | [SymbolicAI/Linq2Z3.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Linq2Z3.ipynb) | Z3, SMT solving |
| CSP-6 Hybridation CP+SAT | [Search/Part2-CSP/CSP-6-Hybridization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-6-Hybridization.ipynb) | SAT encoding |
| CSP-1 Fondamentaux | [Search/Part2-CSP/CSP-1-Fundamentals.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-1-Fundamentals.ipynb) | Modelisation |
| Search-3 A* | [Search/Part1-Foundations/Search-3-Informed.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-3-Informed.ipynb) | Exploration |

### References externes
- Clarke, E., et al. (2001). "Bounded Model Checking Using Satisfiability Solving." *Formal Methods in System Design*, 19(1), 7-34. [Springer](https://link.springer.com/article/10.1023/A:1012796211709)
- CBMC: C Bounded Model Checker. [GitHub](https://github.com/diffblue/cbmc)
- SV-COMP: Competition on Software Verification. [sv-comp.sosy-lab.org](https://sv-comp.sosy-lab.org/)
- Kroening, D., & Strichman, O. (2008). "Decision Procedures: An Algorithmic Point of View." *Springer*. [Springer](https://link.springer.com/book/10.1007/978-3-540-74105-3)

### Difficulte : 3/5

---

## F4 - Compiler fuzzing par generation SMT d'inputs

Le compiler fuzzing consiste a generer automatiquement des programmes d'entree pour tester un compilateur, dans le but de decouvrir des bugs de compilation (crashes, mauvais code genere, optimisations incorrectes). L'approche SMT-based utilise un solveur SMT pour generer des programmes qui couvrent des chemins specifiques du compilateur ou qui satisfont des contraintes de couverture (ex : chaque branche d'un switch doit etre atteinte). C'est une application de la generation sous contraintes a la validation de compilateurs.

### Objectifs
- Implementer un generateur de programmes contraints utilisant Z3 pour creer des inputs de test ciblant un compilateur
- Encoder les contraintes de couverture (branche, chemin, type) comme des formules SMT
- Implementer la generation de programmes C ou LLVM IR satisfaisant les contraintes
- Evaluer sur un compilateur cible (GCC, Clang, ou un compilateur educatif)
- Comparer le taux de decouverte de bugs avec du fuzzing aleatoire (AFL, libFuzzer)

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| Linq2Z3 | [SymbolicAI/Linq2Z3.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Linq2Z3.ipynb) | Z3, contraintes |
| CSP-6 Hybridation CP+SAT | [Search/Part2-CSP/CSP-6-Hybridization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-6-Hybridization.ipynb) | Generation sous contraintes |
| SC-13 Fuzz Testing | [SymbolicAI/SmartContracts/03-Foundry-Testing/SC-13-Fuzz-Invariants.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/SmartContracts/03-Foundry-Testing/SC-13-Fuzz-Invariants.ipynb) | Fuzzing, tests |
| CSP-1 Fondamentaux | [Search/Part2-CSP/CSP-1-Fundamentals.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-1-Fundamentals.ipynb) | Modelisation |

### References externes
- Yang, X., et al. (2011). "Finding and Understanding Bugs in C Compilers." *PLDI*. [ACM](https://dl.acm.org/doi/10.1145/1993498.1993532)
- Csmith: Random C Program Generator. [GitHub](https://github.com/csmith-project/csmith)
- Buchhold, F., et al. (2023). "SMT-Based Generation of Provably Correct Compiler Tests." *TACAS*. [Springer](https://link.springer.com/chapter/10.1007/978-3-031-30820-8_8)
- Livinskii, V., et al. (2020). "Revisiting Compiler Fuzzing." *OOPSLA*. [ACM](https://dl.acm.org/doi/10.1145/3428248)

### Difficulte : 4/5

---

## F5 - Verification SMT de reseaux de regulation genetique

Les reseaux de regulation genetique (Gene Regulatory Networks) modelisent les interactions entre genes, proteines et metabolites dans une cellule. La verification formelle consiste a prouver que ces reseaux satisfont certaines proprietes biologiques (homeostasie, absence d'etats pathologiques, reachabilite d'etats sains) en encodant le reseau comme un systeme de transitions avec des variables booleennes ou entieres, et en verifiant les proprietes avec un solveur SMT. C'est une application fascinante du SAT/SMT a la biologie systemique.

### Objectifs
- Encoder un reseau de regulation genetique ( modele de Thomas ou reseau booleen) comme un systeme de transitions SMT
- Implementer la verification de proprietes de surete (absence d'etats pathologiques) et de vivacite (reachabilite d'etats sains)
- Utiliser Z3 pour explorer l'espace d'etats du reseau et produire des traces d'execution
- Evaluer sur des reseaux de la litterature (cell cycle de la levure, reseau de l'arabidopsis)
- Comparer avec des outils specialises (GINsim, BIOCHAM) pour la modelisation biologique

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| Linq2Z3 | [SymbolicAI/Linq2Z3.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Linq2Z3.ipynb) | Z3, SMT solving |
| CSP-1 Fondamentaux | [Search/Part2-CSP/CSP-1-Fundamentals.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-1-Fundamentals.ipynb) | Modelisation par contraintes |
| Search-1 StateSpace | [Search/Part1-Foundations/Search-1-StateSpace.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-1-StateSpace.ipynb) | Espaces d'etats |
| Probas/ (Infer.NET) | [Probas/](https://github.com/jsboige/CoursIA/tree/main/MyIA.AI.Notebooks/Probas) | Programmation probabiliste |

### References externes
- Bernot, G., et al. (2004). "Application of Formal Methods to Biological Regulatory Networks." *Journal of Theoretical Biology*, 229(3), 339-347. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0022519304002007)
- Thomas, R. (1991). "Regulatory Networks Seen as Asynchronous Automata: A Logical Description." *Journal of Theoretical Biology*, 153(1), 1-23. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0022519305803502)
- GINsim: Gene Regulatory Network Simulator. [ginsim.org](http://ginsim.org/)
- Batt, G., et al. (2005). "Symbolic Reachability Analysis of Genetic Regulatory Networks Using Decision Diagrams." *Bioinformatics*, 21(7), 1101-1107. [Oxford](https://academic.oup.com/bioinformatics/article/21/7/1101/220149)

### Difficulte : 3/5

---

## G1 - Planification temporelle PDDL 2.1 + CP hybride

La planification temporelle etend la planification classique (PDDL) en ajoutant des durees, des fenetres temporelles, et des ressources limitées. Le standard PDDL 2.1 supporte les actions duratives et les contraintes numeriques, mais les solveurs de planification classiques (Fast Downward, LAMA) ont des performances limitees sur les instances a forte composante temporelle. L'approche hybride consiste a utiliser PDDL pour la modelisation de haut niveau, puis a traduire le plan en un probleme CP-SAT (IntervalVar, Cumulative) pour l'optimisation fine des ressources temporelles.

### Objectifs
- Modeliser un probleme de planification temporelle en PDDL 2.1 et le traduire en CP-SAT
- Implementer les actions duratives, les contraintes numeriques et les ressources avec IntervalVar et Cumulative
- Comparer les performances du solveur de planification (Fast Downward temporal) et du solveur CP-SAT
- Etudier les compromis entre expressivite PDDL et efficacite CP-SAT
- Evaluer sur des benchmarks temporels (International Planning Competition, domains temporal)

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| Planners-7 OR-Tools | [SymbolicAI/Planners/03-Advanced/Planners-7-OR-Tools.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Planners/03-Advanced/Planners-7-OR-Tools.ipynb) | PDDL temporel |
| Planners-1 Foundation | [SymbolicAI/Planners/01-Foundation/Planners-1-Introduction.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Planners/01-Foundation/Planners-1-Introduction.ipynb) | PDDL, planification |
| CSP-4 Scheduling | [Search/Part2-CSP/CSP-4-Scheduling.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-4-Scheduling.ipynb) | IntervalVar, Cumulative |
| CSP-6 Hybridation CP+SAT | [Search/Part2-CSP/CSP-6-Hybridization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-6-Hybridization.ipynb) | Hybridation solveurs |

### References externes
- Fox, M., & Long, D. (2003). "PDDL2.1: An Extension to PDDL for Expressing Temporal Planning Domains." *Journal of Artificial Intelligence Research*, 20, 61-124. [JAIR](https://www.jair.org/index.php/jair/article/view/10352)
- Fast Downward: Planning System. [fast-downward.org](https://www.fast-downward.org/)
- Coles, A., et al. (2010). "Forward-Chaining Partial-Order Planning." *ICAPS*. [AAAI](https://ojs.aaai.org/index.php/ICAPS/article/view/17543)
- International Planning Competition: Temporal Track. [icaps-conference.org](https://www.icaps-conference.org/)

### Difficulte : 4/5

---

## G2 - Planification HTN sous contraintes

La planification HTN (Hierarchical Task Network) decompose recursivement une tache complexe en sous-taches elementaires selon des methodes predefinies, contrairement a la planification classique qui recherche un chemin dans l'espace d'etats. L'ajout de contraintes (precedence, ressources, temps) aux methodes HTN produit des plans plus realistes mais augmente la complexite. La modelisation CP-SAT des contraintes HTN permet d'exploiter la structure hierarchique pour guider la recherche et reduire l'espace combinatoire.

### Objectifs
- Modeliser un probleme HTN avec contraintes (precedence, ressources, temps) en CP-SAT
- Implementer la decomposition hierarchique des taches avec des contraintes sur les sous-taches
- Comparer les performances avec un solveur HTN classique (SHOP2, Panda) sur des benchmarks
- Etudier l'ajout de contraintes de ressources (personnel, budget) aux methodes de decomposition
- Evaluer sur des domaines HTN de la litterature (logistique, evacuation, cuisine)

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| Planners-9 HTN Planning | [SymbolicAI/Planners/03-Advanced/Planners-9-HTN.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Planners/03-Advanced/Planners-9-HTN.ipynb) | HTN, decomposition |
| Planners-1 Foundation | [SymbolicAI/Planners/01-Foundation/Planners-1-Introduction.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Planners/01-Foundation/Planners-1-Introduction.ipynb) | Planification classique |
| CSP-4 Scheduling | [Search/Part2-CSP/CSP-4-Scheduling.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-4-Scheduling.ipynb) | Contraintes temporelles |
| CSP-1 Fondamentaux | [Search/Part2-CSP/CSP-1-Fundamentals.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-1-Fundamentals.ipynb) | Modelisation CSP |

### References externes
- Erol, K., et al. (1994). "HTN Planning: Complexity and Expressivity." *AAAI*. [AAAI](https://www.aaai.org/Library/AAAI/1994/aaai94-050.php)
- Nau, D., et al. (2003). "SHOP2: An HTN Planning System." *Journal of Artificial Intelligence Research*, 20, 379-404. [JAIR](https://www.jair.org/index.php/jair/article/view/10302)
- Bercher, P., et al. (2019). "A Survey on Hierarchical Planning." *KI Journal*. [Springer](https://link.springer.com/article/10.1007/s13218-019-00620-5)
- Alford, R., et al. (2016). "An Analysis of the Complexity of HTN Planning via Translation to STRIPS." *ICAPS*. [AAAI](https://ojs.aaai.org/index.php/ICAPS/article/view/13757)

### Difficulte : 4/5

---

## G3 - Coordination de drones par Multi-Agent Path Finding

Le Multi-Agent Path Finding (MAPF) consiste a calculer les trajectoires optimales d'un ensemble d'agents (drones, robots) partageant un espace commun, de maniere a ce qu'aucune collision ne se produise et que chaque agent atteigne son objectif. C'est un probleme combinatoire extremement difficile (NP-hard) qui se modelise naturellement en CP-SAT avec des contraintes de non-collision (pas deux agents au meme noeud au meme instant), de mouvement (deplacement vers les voisins uniquement), et d'objectif (chaque agent doit atteindre sa cible). **Note** : contrairement au Multi-robot Warehouse Task Assignment (annexe #12, EPITA 2025) qui modelise l'affectation de taches dans un entrepot sur grille 2D avec aisles predefinis, ce sujet se concentre sur la coordination de drones en espace aerien ouvert 3D avec contraintes de zones NOTAM, separation ATC (distance minimale en vol libre), conditions meteorologiques dynamiques, et obstacles tridimensionnels (batiments, lignes haute tension). L'espace de recherche est continu (pas de grille) et les contraintes de collision sont tridimensionnelles avec marges de securite.

### Objectifs
- Modeliser le MAPF comme un probleme CP-SAT avec contraintes de non-collision temporelles
- Implementer les contraintes de mouvement (grille 2D/3D), d'objectif et de non-collision (sommet et arete)
- Ajouter des contraintes de capacite (zones a trafic limite) et d'optimisation (minimiser le makespan ou le flowtime)
- Evaluer sur les benchmarks MAPF de la litterature (Moving AI Lab, grid-based)
- Comparer avec les algorithmes specialises MAPF (CBS, A* with OD, ECBS)

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| Search-3 A* | [Search/Part1-Foundations/Search-3-Informed.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-3-Informed.ipynb) | A*, heuristiques |
| CSP-4 Scheduling | [Search/Part2-CSP/CSP-4-Scheduling.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-4-Scheduling.ipynb) | IntervalVar, conflits |
| CSP-9 Distributed CSP | [Search/Part2-CSP/CSP-9-Distributed.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-9-Distributed.ipynb) | Multi-agent, coordination |
| Search-1 StateSpace | [Search/Part1-Foundations/Search-1-StateSpace.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-1-StateSpace.ipynb) | Espaces d'etats |

### References externes
- Stern, R., et al. (2019). "Multi-Agent Pathfinding: Definitions, Variants, and Benchmarks." *Symposium on Combinatorial Search (SoCS)*. [arXiv](https://arxiv.org/abs/1906.08291)
- Sharon, G., et al. (2015). "Conflict-Based Search for Optimal Multi-Agent Pathfinding." *Artificial Intelligence*, 219, 40-66. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0004370214001386)
- Moving AI Lab: MAPF Benchmarks. [movingai.com](https://movingai.com/benchmarks/mapf/)
- Felner, A., et al. (2017). "Adding Heuristics to Conflict-Based Search for Multi-Agent Path Finding." *ICAPS*. [AAAI](https://ojs.aaai.org/index.php/ICAPS/article/view/13826)

### Difficulte : 3/5

---

## G4 - Apprentissage d'heuristiques pour solveurs CP

L'apprentissage d'heuristiques (Learning to Search) consiste a entrainer un modele de machine learning (reseau de neurones, arbre de decision) pour predire les meilleures decisions de branchement dans un solveur CP, remplacant les heuristiques manuellement designees. Le solveur CP-SAT de Google utilise deja un composant ML pour le choix des variables (branching), et ce sujet explore comment ameliorer ou specialiser cette approche pour une classe de problemes donnee. C'est un sujet a l'interface ML/CP qui requiert une bonne comprehension des deux domaines.

### Objectifs
- Comprendre les heuristiques de branchement dans les solveurs CP (VSIDS, activity, first-fail) et les encoder comme features ML
- Collecter des donnees d'apprentissage en executant le solveur sur des instances de reference et en enregistrant les decisions optimales
- Entrainer un modele ( Gradient Boosting ou petit reseau de neurones) pour predire la variable a brancher
- Integrer le modele dans un solveur CP (CPMpy ou mini-solveur custom) et evaluer l'impact sur les performances
- Comparer les performances (temps de resolution, noeuds explores) avec les heuristiques par defaut

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-6 Hybridation CP+SAT | [Search/Part2-CSP/CSP-6-Hybridization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-6-Hybridization.ipynb) | Solveurs, heuristiques |
| CSP-1 Fondamentaux | [Search/Part2-CSP/CSP-1-Fundamentals.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-1-Fundamentals.ipynb) | Propagation, branchement |
| Search-3 A* | [Search/Part1-Foundations/Search-3-Informed.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-3-Informed.ipynb) | Heuristiques |
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Optimisation, benchmarks |

### References externes
- Bengio, Y., et al. (2021). "Machine Learning for Combinatorial Optimization: A Methodological Tour d'Horizon." *European Journal of Operational Research*, 290(2), 405-421. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0377221720306901)
- Cappart, Q., et al. (2021). "Combining Reinforcement Learning and Constraint Programming for Combinatorial Optimization." *AAAI*. [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/17739)
- Balcan, M., et al. (2021). "Data-Driven Algorithm Design." *Annual Review of Computer Science*. [Annual Reviews](https://www.annualreviews.org/doi/10.1146/annurev-computersci-012420-101047)
- Gasse, M., et al. (2019). "Exact Combinatorial Optimization with Graph Convolutional Neural Networks." *NeurIPS*. [arXiv](https://arxiv.org/abs/1906.01629)

### Difficulte : 4/5

---

## H1 - Composition musicale assistee par contraintes

La composition musicale assistee par contraintes consiste a generer des partitions musicales (melodies, harmonies, contrepoint) satisfaisant un ensemble de regles musicales encodees comme des contraintes : regles d'harmonie (accords permis, progressions), de contrepoint (mouvements contraires, intervalles permis), de rythme (metrique, syncope), et de style (tonalite, mode). Ce sujet explore la musique comme un espace de solutions sous contraintes, ou la creativite emerge de la combinaison de regles strictes et de preferences esthetiques.

### Objectifs
- Modeliser les regles d'harmonie tonale et de contrepoint comme des contraintes CP-SAT sur les hauteurs, durees et accords
- Implementer les contraintes de mouvement (paralleles interdits, resolutions), de metrique et de tessiture
- Ajouter des soft constraints pour les preferences stylistiques (style baroque, jazz, contemporain)
- Generer des partitions en notation ABC ou MIDI et les rendre ecoutables
- Evaluer qualitativement avec des musiciens et quantitativement (respect des regles, diversite)

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-1 Fondamentaux | [Search/Part2-CSP/CSP-1-Fundamentals.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-1-Fundamentals.ipynb) | Modelisation CSP |
| CSP-7 Soft Constraints | [Search/Part2-CSP/CSP-7-Soft.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-7-Soft.ipynb) | Preferences, penalites |
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Optimisation |
| Search-4 Local Search | [Search/Part1-Foundations/Search-4-LocalSearch.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-4-LocalSearch.ipynb) | Recherche locale |

### References externes
- Anders, T. (2009). "Composing Music by Composing Rules: Computer-Assisted Composition Using Constraint Programming." *PhD Thesis, Queen Mary University of London*. [QMUL](https://ethos.bl.uk/OrderDetails.do?uin=uk.bl.ethos.509680)
- Truchet, C., & Codognet, P. (2004). "Musical Constraint Satisfaction Problems Applied to Harmony." *Constraints*, 9(1), 23-44. [Springer](https://link.springer.com/article/10.1023/B:CONS.0000004893.29957.51)
- Strasila: Constraint-Based Music Composition. [GitHub](https://github.com/tanders/strasila)
- Ames, C. (1989). "The Markov Process as a Compositional Model." *Computer Music Journal*, 13(1), 6-13. [JSTOR](https://www.jstor.org/stable/3679856)
- Turczan, G. (2020). "Toward an Adaptive Real-Time System for Spatialization and Processing of Live Electronic Music." *MFA Thesis, CalArts*. [PDF](https://mtiid.calarts.edu/wp-content/uploads/2020/03/Turczan_MFA_Thesis.pdf)
- Scale Navigator — exploration interactive des gammes et modes musicaux. [dashboard.scalenavigator.com](https://dashboard.scalenavigator.com)

### Difficulte : 3/5

---

## H2 - Generation procedurale de niveaux de jeu (WFC)

La generation procedurale de niveaux par Wave Function Collapse (WFC) consiste a generer des grilles 2D ou 3D (cartes de jeu, donjons, villes) a partir d'un ensemble de tuiles avec des contraintes d'adjacence (quelle tuile peut etre placee a cote de quelle autre). WFC est essentiellement un algorithme de propagation de contraintes (AC-4) avec backtracking, ce qui en fait un sujet ideal pour explorer les liens entre CP et generation de contenu. L'extension CP-SAT permet d'ajouter des contraintes globales (connectivite, difficulte, esthetique) que WFC pur ne supporte pas.

### Objectifs
- Implementer WFC comme un probleme de satisfaction de contraintes avec CP-SAT (variables = tuiles, contraintes = adjacence)
- Ajouter des contraintes globales : connectivite du niveau, chemin du joueur, placement d'objets
- Implementer des contraintes de difficulte (densite d'ennemis, complexite du parcours) et de variete
- Evaluer sur des ensembles de tuiles existants ( ressources Unity/Godot, WaveFunctionCollapse repo)
- Comparer la qualite et la diversite des niveaux generes par WFC pur, CP-SAT, et generation aleatoire

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-1 Fondamentaux | [Search/Part2-CSP/CSP-1-Fundamentals.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-1-Fundamentals.ipynb) | Propagation de contraintes |
| Search-4 Local Search | [Search/Part1-Foundations/Search-4-LocalSearch.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-4-LocalSearch.ipynb) | Recherche locale |
| CSP-7 Soft Constraints | [Search/Part2-CSP/CSP-7-Soft.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-7-Soft.ipynb) | Preferences |
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Optimisation |

### References externes
- Karth, I., & Smith, A.M. (2017). "WaveFunctionCollapse is Constraint Solving in the Wild." *PCG Workshop at FDG'17*. [ACM DL](https://dl.acm.org/doi/10.1145/3102071.3110566)
- WaveFunctionCollapse (original implementation). [GitHub](https://github.com/mxgmn/WaveFunctionCollapse)
- Tabor, J. (2022). "Constraint-Based Procedural Generation: A Survey." *IEEE Transactions on Games*. [IEEE](https://ieeexplore.ieee.org/document/9792255)
- Smith, A.M., & Mateas, M. (2011). "Answer Set Programming for Procedural Content Generation." *IEEE T-CIAIG*. [IEEE](https://ieeexplore.ieee.org/document/5668232)

### Difficulte : 3/5

---

## H3 - Cryptanalyse par contraintes (ciphers avances)

La cryptanalyse par contraintes consiste a utiliser la programmation par contraintes pour casser (ou analyser la securite de) chiffrements classiques et avances : substitution monoalphabetique, Vigenere, transposition, Hill cipher, et chiffrements par blocs reduits. Contrairement a la cryptanalyse statistique classique (analyse de frequence), l'approche CP encode les proprietes du chiffre et du langage comme des contraintes, permettant de chercher systematiquement la cle dans l'espace des solutions possibles.

### Objectifs
- Modeliser differents types de chiffrements (substitution, Vigenere, transposition, Hill) comme des problemes CSP
- Implementer les contraintes linguistiques (bigrammes, trigrammes frequents, dictionnaire) pour guider la recherche
- Ajouter des contraintes de structure de cle (longueur, caracteres permis) et de texte clair (langue connue)
- Comparer les performances de CP-SAT avec l'analyse de frequence classique et la force brute
- Evaluer sur des textes chiffres de reference (cryptogrammes, challenges ACA)

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-1 Fondamentaux | [Search/Part2-CSP/CSP-1-Fundamentals.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-1-Fundamentals.ipynb) | Modelisation CSP |
| Sudoku-12 Z3 Python | [Sudoku/Sudoku-12-Z3-Python.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Sudoku/Sudoku-12-Z3-Python.ipynb) | Resolution par contraintes |
| Linq2Z3 | [SymbolicAI/Linq2Z3.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Linq2Z3.ipynb) | Z3, raisonnement |
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Optimisation |

### References externes
- Biondi, P., et al. (2022). "Crypyographic Constraint Solving with CryptoMiniSat." *SAC*. [ACM](https://dl.acm.org/doi/10.1145/3471999)
- Lucks, M. (1990). "A Constraint-Based Cipher." *Eurocrypt*. [IACR](https://link.springer.com/chapter/10.1007/3-540-46877-3_16)
- American Cryptogram Association (ACA) - Cipher Types and Samples. [cryptogram.org](https://www.cryptogram.org/)
- simonbyrne/libconstraint-crypto: Constraint-based cipher breaking. [GitHub](https://github.com/simonbyrne/libconstraint-crypto)

### Difficulte : 3/5

---

## H4 - Covering Arrays avec contraintes semantiques

Les Covering Arrays (CA) sont des matrices N x k ou chaque colonne represente un parametre (facteur) avec v valeurs, telles que toute combinaison de t colonnes contienne tous les t-uplets possibles au moins une fois. Les CA sont utilises pour les tests combinatoires de logiciels (t-way testing) : au lieu de tester toutes les combinaisons (v^k), on teste un sous-ensemble qui couvre toutes les interactions de t parametres. L'ajout de contraintes semantiques (certaines combinaisons sont interdites car impossibles dans le systeme reel) rend le probleme plus difficile et plus interessant. **Note** : contrairement a l'Automatic Tests Generation basique (annexe #19, EPITA 2025) qui generait des tests unitaires automatiques via analyse de code, ce sujet se concentre sur la construction de Covering Arrays avec t >= 3 (au-dela du pairwise classique), des contraintes semantiques entre parametres (combinaisons interdites exprimees en logique propositionnelle), et la minimisation exacte du nombre de lignes N. L'approche CP-SAT est structurellement differente de la generation de tests : il s'agit d'un probleme d'optimisation combinatoire pur (minimiser N sujet a couverture t-way complete), pas de generation de code de test.

### Objectifs
- Modeliser la construction de Covering Arrays (t-way) comme un probleme d'optimisation avec CP-SAT
- Implementer les contraintes de couverture t-way et les contraintes semantiques (combinaisons interdites)
- Ajouter l'optimisation du nombre de lignes N (minimisation) et la prise en compte des contraintes d'exclusion
- Evaluer sur des configurations reelles (systemes embarques, APIs REST, interfaces graphiques)
- Comparer avec les algorithmes gloutons (IPOG, AETG) et les bornes inferieures theoriques

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-1 Fondamentaux | [Search/Part2-CSP/CSP-1-Fundamentals.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-1-Fundamentals.ipynb) | Modelisation CSP |
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Optimisation combinatoire |
| Search-4 Local Search | [Search/Part1-Foundations/Search-4-LocalSearch.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-4-LocalSearch.ipynb) | Heuristiques |
| SC-13 Fuzz Testing | [SymbolicAI/SmartContracts/03-Foundry-Testing/SC-13-Fuzz-Invariants.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/SmartContracts/03-Foundry-Testing/SC-13-Fuzz-Invariants.ipynb) | Generation de tests |

### References externes
- Hartman, A., & Raskin, L. (2004). "Problems and Algorithms for Covering Arrays." *Discrete Mathematics*, 284(1-3), 149-156. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0012365X04000980)
- Cohen, M.B., et al. (2003). "Constructing Test Suites for Interaction Testing." *ICSE*. [IEEE](https://ieeexplore.ieee.org/document/1205210)
- Nie, C., & Leung, H. (2011). "A Survey of Combinatorial Testing." *ACM Computing Surveys*, 43(2). [ACM](https://dl.acm.org/doi/10.1145/1883612.1883618)
- NIST: Combinatorial Testing. [nist.gov](https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software)

### Difficulte : 3/5

---

## I1 - Assistant de planification conversationnel (LLM + CSP)

Un assistant de planification conversationnel combine un modele de langage (LLM) pour l'interaction en langage naturel avec un solveur CP-SAT pour la resolution de contraintes. L'utilisateur decrit sa demande en langage naturel ("Je veux organiser un voyage de 5 jours a Rome avec un budget de 2000 euros"), le LLM extrait les contraintes et les parametres, le solveur CP-SAT genere un plan optimal, et le LLM presente le resultat de maniere comprehensible. Le coeur du sujet est la modelisation CP (min 5 types de contraintes, instance reelle), le LLM n'etant que l'interface.

### Objectifs
- Concevoir un schema d'extraction de contraintes a partir de langage naturel via un LLM (function calling, prompt structure)
- Implementer un modele CP-SAT avec au moins 5 types de contraintes pour un domaine concret (planning de voyage, ordonnancement, allocation)
- Gerer les interactions multi-tours : raffinement des contraintes, ajout de preferences, explication des compromis
- Evaluer la robustesse de l'extraction LLM (taux de conversion correcte, gestion des ambiguites)
- Comparer avec une interface contrainte (formulaire) pour mesurer l'apport du langage naturel

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-6 Hybridation CP+SAT | [Search/Part2-CSP/CSP-6-Hybridization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-6-Hybridization.ipynb) | LLM+CSP, hybridation |
| CSP-4 Scheduling | [Search/Part2-CSP/CSP-4-Scheduling.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-4-Scheduling.ipynb) | IntervalVar, planning |
| CSP-7 Soft Constraints | [Search/Part2-CSP/CSP-7-Soft.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-7-Soft.ipynb) | Preferences, compromis |
| App-17 VRP Logistics | [Search/Applications/Hybrid/App-17-VRP-Logistics.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Applications/Hybrid/App-17-VRP-Logistics.ipynb) | Planning, optimisation |

### References externes
- Ahmetovic, D., et al. (2023). "LLM as a Cognitive Assistant for Constraint Modeling." *CP Conference*. [Springer](https://link.springer.com/chapter/10.1007/978-3-031-47361-5_2)
- OpenAI Function Calling Guide. [OpenAI](https://platform.openai.com/docs/guides/function-calling)
- Google. "CP-SAT Solver Documentation." [developers.google.com](https://developers.google.com/optimization/cp/cp_solver)
- Model Context Protocol (MCP) Specification. [MCP](https://modelcontextprotocol.io/)

### Difficulte : 3/5

---

## I2 - Explicateur de solutions CP par LLM

L'explication de solutions CP consiste a generer des explications en langage naturel qui decrivent pourquoi une solution donnee est optimale (ou pourquoi aucune solution n'existe), quelles contraintes sont actives (binding), et comment modifier les contraintes pour obtenir un meilleur resultat. L'approche combine l'analyse des contraintes du solveur (shadows prices, conflict analysis) avec un LLM pour produire des explications comprehensibles par un non-expert. C'est un pont entre l'optimisation mathematique et l'intelligence artificielle dialoguee.

### Objectifs
- Extraire les informations structurelles d'une solution CP-SAT (contraintes actives, marges, conflits)
- Concevoir un pipeline d'explication : analyse du solveur, structuration des faits, generation en langage naturel
- Implementer les explications de type "pourquoi cette solution", "pourquoi pas X", et "comment ameliorer"
- Evaluer la qualite des explications avec des metriques automatiques et une evaluation humaine
- Comparer avec des explications template-based (sans LLM) sur la clarte et la precision

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-6 Hybridation CP+SAT | [Search/Part2-CSP/CSP-6-Hybridization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-6-Hybridization.ipynb) | LLM+CSP |
| CSP-1 Fondamentaux | [Search/Part2-CSP/CSP-1-Fundamentals.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-1-Fundamentals.ipynb) | Modelisation, solutions |
| CSP-7 Soft Constraints | [Search/Part2-CSP/CSP-7-Soft.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-7-Soft.ipynb) | Compromis, marges |
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Optimalite |

### References externes
- Cyras, K., et al. (2021). "Explainable Constraint-Driven Scheduling." *AAAI*. [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/16677)
- Fox, M., et al. (2017). "Explainable Planning." *IJCAI Workshop on XAI*. [arXiv](https://arxiv.org/abs/1709.10256)
- Guidotti, R., et al. (2018). "A Survey of Methods for Explaining Black Box Models." *ACM Computing Surveys*, 51(5). [ACM](https://dl.acm.org/doi/10.1145/3236009)
- Rago, A., et al. (2023). "Argumentative Explanations for Constraint Optimization." *KR*. [CEUR](https://ceur-ws.org/Vol-3361/)

### Difficulte : 3/5

---

## I3 - Modelisation CP assistee par LLM

La modelisation CP assistee par LLM consiste a utiliser un modele de langage pour transformer automatiquement une description en langage naturel d'un probleme d'optimisation en un modele CP-SAT executable. Le defi est de capturer les contraintes implicites (celles que le formulateur oublie de mentionner car evidentes pour lui), de choisir les bonnes variables de decision, et de generer un code correct. Ce sujet est a l'avant-garde de la recherche en IA symbolique/neuro-symbolique et requiert une maitrise solide de la modelisation CP.

### Objectifs
- Concevoir un pipeline de transformation NL vers CP-SAT : analyse du probleme, identification des variables, extraction des contraintes, generation du code
- Implementer la verification de correction du modele genere (propriétés de base : faisabilite, bornes, symetries)
- Evaluer sur un benchmark de problemes d'optimisation decrits en langage naturel (10+ problemes variés)
- Analyser les echecs de generation (contraintes manquantes, variables incorrectes) et proposer des strategies de correction
- Comparer avec la modelisation manuelle par un expert CP (qualite, temps, couverture des contraintes)

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-6 Hybridation CP+SAT | [Search/Part2-CSP/CSP-6-Hybridization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-6-Hybridization.ipynb) | LLM+CSP |
| CSP-1 Fondamentaux | [Search/Part2-CSP/CSP-1-Fundamentals.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-1-Fundamentals.ipynb) | Modelisation |
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Optimisation |
| Search-9 Programmation lineaire | [Search/Part1-Foundations/Search-9-LinearProgramming.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-9-LinearProgramming.ipynb) | Formulation mathematique |

### References externes
- Ahmetovic, D., et al. (2023). "LLM as a Cognitive Assistant for Constraint Modeling." *CP Conference*. [Springer](https://link.springer.com/chapter/10.1007/978-3-031-47361-5_2)
- Nethercote, N., Stuckey, P.J., Becket, R., Brand, S., Duck, G.J., & Tack, G. (2007). "MiniZinc: Towards a Standard CP Modelling Language." *Principles and Practice of Constraint Programming (CP 2007)*. [Springer](https://link.springer.com/chapter/10.1007/978-3-540-74970-7_38)
- Cappart, Q., et al. (2023). "A Survey on the Integration of Machine Learning and Constraint Programming." *Constraints*. [Springer](https://link.springer.com/article/10.1007/s10601-023-09348-7)
- GCode: Generating Optimization Code from Natural Language. [GitHub](https://github.com/optsuite/gcode)

### Difficulte : 4/5

---

## J1 - Allocation multicritere de candidats

L'allocation multicritere de candidats consiste a affecter des candidats a des postes (ou des etudiants a des projets, des employes a des equipes) en tenant compte de multiples criteres : competences, preferences, disponibilite, diversite, equite. C'est une extension du probleme de Stable Marriage avec des criteres multiples et des contraintes de capacite. La modelisation CP-SAT permet de capturer les contraintes dures (competences minimum, quotas de diversite) et les preferences comme soft constraints avec ponderation.

### Objectifs
- Modeliser l'allocation multicritere comme un probleme d'affectation avec preferences et contraintes de capacite en CP-SAT
- Implementer les contraintes de competences (matching skills/requirements), de diversite (quotas), et d'equite
- Ajouter les preferences des candidats et des recruteurs comme soft constraints avec penalites ponderees
- Evaluer sur des instances reelles ou synthetiques (donnees RH, affectation d'etudiants)
- Comparer avec l'algorithme de Gale-Shapley (Stable Marriage) et un modele PLNE

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| GameTheory/ | [GameTheory/](https://github.com/jsboige/CoursIA/tree/main/MyIA.AI.Notebooks/GameTheory) | Stable Marriage, Shapley Value |
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Affectation, optimisation |
| CSP-7 Soft Constraints | [Search/Part2-CSP/CSP-7-Soft.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-7-Soft.ipynb) | Preferences, penalites |
| CSP-1 Fondamentaux | [Search/Part2-CSP/CSP-1-Fundamentals.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-1-Fundamentals.ipynb) | Modelisation CSP |

### References externes
- Gale, D., & Shapley, L.S. (1962). "College Admissions and the Stability of Marriage." *American Mathematical Monthly*, 69(1), 9-15. [JSTOR](https://www.jstor.org/stable/2312726)
- Manlove, D.F. (2013). "Algorithmics of Matching Under Preferences." *World Scientific*. [World Scientific](https://www.worldscientific.com/worldscibooks/10.1142/8591)
- Drummond, J., & Boutilier, C. (2014). "Elicitation and Approximately Stable Matching with Partial Preferences." *AAMAS*. [ACM](https://dl.acm.org/doi/10.5555/2615731.2616062)
- Irving, R.W. (1998). "Matching Medical Students to Pairs of Hospitals." *Algorithmica*, 20, 129-143. [Springer](https://link.springer.com/article/10.1007/PL00009189)

### Difficulte : 3/5

---

## J2 - Enchere combinatoire et Winner Determination

L'enchere combinatoire permet aux soumissionnaires de placer des offres sur des combinaisons d'items (et non sur des items individuels), capturant ainsi les synergies et les complementarites. Le probleme du Winner Determination (WDP) consiste a determiner l'ensemble d'offres gagnantes qui maximise les revenus du vendeur, sous la contrainte qu'un item ne peut etre attribue qu'une seule fois. C'est un probleme d'optimisation combinatoire (Set Packing) qui se modelise directement en CP-SAT ou PLNE, avec des applications dans les telecommunications (spectre 5G), la logistique et les marches publics.

### Objectifs
- Modeliser le Winner Determination Problem comme un Set Packing avec CP-SAT (variables binaires par offre)
- Implementer les contraintes d'exclusivite (un item = au plus une offre gagnante) et de budget
- Ajouter les contraintes de type XOR (un soumissionnaire ne peut gagner qu'une offre parmi un groupe)
- Evaluer sur les benchmarks CATS (Combinatorial Auction Test Suite) et comparer avec un modele PLNE
- Etendre aux encheres VCG (Vickrey-Clarke-Groves) pour calculer les paiements optimaux

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| GameTheory/ | [GameTheory/](https://github.com/jsboige/CoursIA/tree/main/MyIA.AI.Notebooks/GameTheory) | Encheres, Mechanism Design |
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Set Packing, Knapsack |
| CSP-1 Fondamentaux | [Search/Part2-CSP/CSP-1-Fundamentals.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-1-Fundamentals.ipynb) | Modelisation |
| Search-9 Programmation lineaire | [Search/Part1-Foundations/Search-9-LinearProgramming.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-9-LinearProgramming.ipynb) | PLNE, relaxation |

### References externes
- Cramton, P., et al. (2006). "Combinatorial Auctions." *MIT Press*. [MIT Press](https://mitpress.mit.edu/9780262033428/combinatorial-auctions/)
- Leyton-Brown, K., et al. (2000). "CATS: Combinatorial Auction Test Suite." *EC*. [UMich](https://www.cs.ubc.ca/~kevinlb/CATS/)
- Rothkopf, M.H., et al. (1998). "Computationally Manageable Combinatorial Auctions." *Management Science*, 44(8), 1131-1147. [INFORMS](https://pubsonline.informs.org/doi/abs/10.1287/mnsc.44.8.1131)
- Sandholm, T. (2002). "Algorithm for Optimal Winner Determination in Combinatorial Auctions." *Artificial Intelligence*, 135(1-2), 1-54. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0004370201001592)

### Difficulte : 4/5

---

## J3 - Allocation de ressources par mecanisme incitatif

L'allocation de ressources par mecanisme incitatif (Mechanism Design) consiste a concevoir des regles d'allocation qui incitent les agents a reveler leurs vraies preferences (truthfulness), tout en maximisant le bien-etre social ou les revenus. Le probleme central est le Winner Determination (calcul de l'allocation optimale) sous contraintes de veracite (incentive compatibility). La modelisation CP-SAT permet de capturer les contraintes d'allocation (capacite, budget) et d'optimiser le bien-etre social sous contraintes d'incitation.

### Objectifs
- Modeliser le probleme d'allocation avec mecanisme incitatif comme un probleme d'optimisation sous contraintes en CP-SAT
- Implementer les contraintes d'allocation (capacite, budget, exclusivite) et d'incitation (veracite)
- Calculer les paiements VCG (Vickrey-Clarke-Groves) pour garantir la veracite
- Evaluer sur des scenarios d'allocation de ressources publics (spectre radio, periodes de vol, logements)
- Comparer avec des mecanismes non-incitatifs (enchere au premier prix) sur l'efficacite et l'equite

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| GameTheory/ | [GameTheory/](https://github.com/jsboige/CoursIA/tree/main/MyIA.AI.Notebooks/GameTheory) | Mechanism Design, Nash |
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Allocation, optimisation |
| CSP-7 Soft Constraints | [Search/Part2-CSP/CSP-7-Soft.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-7-Soft.ipynb) | Compromis, equite |
| CSP-1 Fondamentaux | [Search/Part2-CSP/CSP-1-Fundamentals.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-1-Fundamentals.ipynb) | Modelisation |

### References externes
- Nisan, N., & Ronen, A. (2001). "Algorithmic Mechanism Design." *Games and Economic Behavior*, 35(1-2), 166-196. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0899825600908669)
- Vickrey, W. (1961). "Counterspeculation, Auctions, and Competitive Sealed Tenders." *Journal of Finance*, 16(1), 8-37. [Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.1961.tb02789.x)
- Clarke, E.H. (1971). "Multipart Pricing of Public Goods." *Public Choice*, 11, 17-33. [Springer](https://link.springer.com/article/10.1007/BF01426210)
- Roughgarden, T. (2016). "Twenty Lectures on Algorithmic Game Theory." *Cambridge University Press*. [Cambridge](https://www.cambridge.org/core/books/twenty-lectures-on-algorithmic-game-theory/)

### Difficulte : 4/5

---

## K1 - Planification urbaine et placement d'infrastructures

La planification urbaine sous contraintes consiste a determiner l'emplacement optimal d'infrastructures (hopitaux, ecoles, centres commerciaux, parcs, stations de recharge) dans une zone urbaine, en maximisant la couverture de la population sous des contraintes de budget, de superficie disponible, de distance maximum aux residents, et de compatibilite entre infrastructures. C'est un probleme de theorie de la localisation (p-median, p-center, MCLP) directement modelisable en CP-SAT avec des variables binaires de localisation et des contraintes de couverture.

### Objectifs
- Modeliser le placement d'infrastructures comme un probleme de localisation (p-median/MCLP) avec CP-SAT
- Implementer les contraintes de budget, de superficie, de distance maximum et de compatibilite entre sites
- Ajouter les contraintes de couverture equitable (minimiser la variance d'accessibilite entre quartiers)
- Evaluer sur des donnees urbaines reelles (OpenStreetMap, donnees INSEE) et des benchmarks synthetiques
- Visualiser les solutions sur une carte (folium, geopandas) pour faciliter l'analyse

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Allocation, localisation |
| CSP-1 Fondamentaux | [Search/Part2-CSP/CSP-1-Fundamentals.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-1-Fundamentals.ipynb) | Modelisation CSP |
| Search-9 Programmation lineaire | [Search/Part1-Foundations/Search-9-LinearProgramming.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-9-LinearProgramming.ipynb) | PLNE, localisation |
| CSP-7 Soft Constraints | [Search/Part2-CSP/CSP-7-Soft.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-7-Soft.ipynb) | Equite, preferences |

### References externes
- Church, R., & ReVelle, C. (1974). "The Maximal Covering Location Problem." *Papers of the Regional Science Association*, 32, 101-118. [Springer](https://link.springer.com/chapter/10.1007/978-3-642-51081-8_6)
- Current, J., et al. (2002). "Facility Location: Applications and Theory." *Springer*. [Springer](https://link.springer.com/book/10.1007/978-3-642-56038-7)
- Daskin, M.S. (2013). "Network and Discrete Location." *Wiley*. [Wiley](https://www.wiley.com/en-us/Network+and+Discrete+Location%3A+Models%2C+Algorithms%2C+and+Applications%2C+2nd+Edition-p-9780470905364)
- Murray, A.T. (2016). "Maximal Coverage Location Problem: Impacts, Significance, and Evolution." *International Regional Science Review*, 39(1), 5-27. [SAGE](https://journals.sagepub.com/doi/abs/10.1177/0160017615607229)

### Difficulte : 3/5

---

## K2 - Allocation de frequences radio

L'allocation de frequences radio (Frequency Assignment Problem, FAP) consiste a attribuer des frequences a des emetteurs radio de maniere a minimiser les interferences, sous des contraintes d'ecart minimal entre frequences d'emetteurs adjacents (geographiquement proches), de spectre disponible (bande de frequences limitee), et de demande variable. C'est un probleme de coloration de graphe contraint qui se modelise naturellement en CSP : chaque emetteur est une variable, chaque frequence est une valeur, et les contraintes d'ecart sont des contraintes binaires.

### Objectifs
- Modeliser le FAP comme un probleme de coloration de graphe contraint avec CP-SAT
- Implementer les contraintes d'ecart (co-channel, adjacent channel), de spectre (bande limitee), et de demande
- Ajouter la minimisation de l'interference totale (somme des violations ponderees) comme soft constraint
- Evaluer sur les benchmarks COST 259 et GRAPH-BASE de la litterature
- Comparer avec DSATUR (coloration gloutonne) et un modele PLNE

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-1 Fondamentaux | [Search/Part2-CSP/CSP-1-Fundamentals.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-1-Fundamentals.ipynb) | Coloration, CSP |
| CSP-7 Soft Constraints | [Search/Part2-CSP/CSP-7-Soft.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-7-Soft.ipynb) | Minimisation violations |
| Search-4 Local Search | [Search/Part1-Foundations/Search-4-LocalSearch.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-4-LocalSearch.ipynb) | Heuristiques de coloration |
| App-8 MiniZinc | [Search/Applications/CSP/App-8-MiniZinc.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Applications/CSP/App-8-MiniZinc.ipynb) | Modelisation MiniZinc |

### References externes
- Aardal, K.I., et al. (2007). "Models and Solution Techniques for Frequency Assignment Problems." *4OR*, 5(4), 261-317. [Springer](https://link.springer.com/article/10.1007/s10288-007-0048-4)
- Hale, W.K. (1980). "Frequency Assignment: Theory and Applications." *Proceedings of the IEEE*, 68(12), 1497-1514. [IEEE](https://ieeexplore.ieee.org/document/1457947)
- COST 259: Wireless Flexible Personalised Communications. [IEEE](https://ieeexplore.ieee.org/xpl/conhome/10000/proceeding)
- CSPLib Problem 020: Frequency Assignment. [csplib.org](https://www.csplib.org/Problems/prob020/)

### Difficulte : 3/5

---

## K3 - Optimisation multiobjectif sous contraintes

L'optimisation multiobjectif sous contraintes consiste a optimiser simultanement plusieurs objectifs contradictoires (minimiser le cout et maximiser la qualite, minimiser le temps et maximiser la couverture) sous des contraintes de faisabilite. La solution n'est pas un optimum unique mais un ensemble de solutions Pareto-optimales (aucun objectif ne peut etre ameliore sans degrader un autre). CP-SAT supporte nativement l'optimisation multiobjectif par ponderation ou epsilon-constraint. Ce sujet est transversal et s'applique a de nombreux domaines (logistique, energie, finance).

### Objectifs
- Implementer l'optimisation multiobjectif en CP-SAT via ponderation, epsilon-constraint, ou Pareto front
- Modeliser un probleme concret avec 3+ objectifs contradictoires (ex : cout, temps, qualite, impact environnemental)
- Calculer et visualiser le front de Pareto (ensemble des solutions non dominees)
- Implementer des strategies de navigation dans le front de Pareto (preference-based, interactive)
- Comparer les approches de resolution (ponderation fixe, epsilon-constraint, NSGA-II hybride)

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Optimisation, objectifs multiples |
| CSP-7 Soft Constraints | [Search/Part2-CSP/CSP-7-Soft.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-7-Soft.ipynb) | Compromis, penalites |
| App-10 Portfolio | [Search/Applications/Hybrid/App-10-Portfolio.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Applications/Hybrid/App-10-Portfolio.ipynb) | Optimisation multiobjectif (rendement/risque) |
| Search-11 Metaheuristiques | [Search/Part1-Foundations/Search-11-Metaheuristics.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-11-Metaheuristics.ipynb) | NSGA-II, metaheuristiques |

### References externes
- Deb, K., et al. (2002). "A Fast and Elitist Multiobjective Genetic Algorithm: NSGA-II." *IEEE Transactions on Evolutionary Computation*, 6(2), 182-197. [IEEE](https://ieeexplore.ieee.org/document/996017)
- Miettinen, K. (1999). "Nonlinear Multiobjective Optimization." *Springer*. [Springer](https://link.springer.com/book/10.1007/978-1-4615-5563-6)
- OR-Tools CP-SAT: Multi-Objective Optimization. [Google Developers](https://developers.google.com/optimization/cp/cp_solver#multi_objective)
- Coello, C.A.C., et al. (2007). "Evolutionary Algorithms for Solving Multi-Objective Problems." *Springer*, 2nd Edition. [Springer](https://link.springer.com/book/10.1007/978-0-387-36797-2)

### Difficulte : 4/5

---

## L1 - Participation a une competition CP/SAT/SMT

Ce meta-sujet consiste a participer a une competition academique de programmation par contraintes (MiniZinc Challenge, SAT Competition, SMT Competition, MaxSAT Evaluation, CSP Competition) en implementant un solveur, un encodeur, ou une heuristique competif. La participation seule ne suffit pas : le livrable doit inclure une analyse des choix techniques, une comparaison avec l'etat de l'art, et une documentation des innovations apportees. Ce sujet est ideal pour les etudiants voulant aller en profondeur sur un aspect specifique du solving.

### Objectifs
- Choisir une competition cible et comprendre les regles, les formats d'entree/sortie, et les metriques d'evaluation
- Implementer un composant competif (solveur, encodeur, preprocesseur, ou heuristique)
- Analyser les performances sur les instances de competition (scaling, robustesse, forces/faiblesses)
- Documenter les innovations techniques et les comparer avec les approches de la litterature
- Produire un rapport detaille incluant les resultats, les analyses, et les pistes d'amelioration

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-6 Hybridation CP+SAT | [Search/Part2-CSP/CSP-6-Hybridization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-6-Hybridization.ipynb) | Solveurs, encodage |
| CSP-1 Fondamentaux | [Search/Part2-CSP/CSP-1-Fundamentals.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-1-Fundamentals.ipynb) | Modelisation |
| App-8 MiniZinc | [Search/Applications/CSP/App-8-MiniZinc.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Applications/CSP/App-8-MiniZinc.ipynb) | MiniZinc, benchmarks |
| Linq2Z3 | [SymbolicAI/Linq2Z3.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Linq2Z3.ipynb) | SMT solving |

### References externes
- SAT Competition. [satcompetition.github.io](https://satcompetition.github.io/)
- MiniZinc Challenge. [minizinc.org](https://www.minizinc.org/challenge.html)
- SMT Competition. [smtcomp.github.io](https://smtcomp.github.io/)
- MaxSAT Evaluation. [maxsat-evaluations.github.io](https://maxsat-evaluations.github.io/)
- Biere, A., et al. (2021). "Handbook of Satisfiability." *IOS Press*, 2nd Edition. [IOS Press](https://iospress.nl/book/handbook-of-satisfiability-2/)

### Difficulte : Variable

---

## M1 - Portefeuille parcimonieux sous contraintes de cardinalite (Sparse Markowitz)

Le portefeuille Mean-Variance de Markowitz (1952) est un classique de la finance quantitative mais souffre, dans sa forme continue, de produire des solutions avec des centaines de lignes de faible poids difficilement gerables en pratique. L'**extension sparse** ajoute une contrainte de cardinalite K (exactement K titres actifs parmi N candidats) qui transforme le probleme en un programme quadratique mixte entier (MIQP), non convexe et NP-difficile. Ce sujet explore sa modelisation en CP-SAT (linearisation SOS1), en MILP (Big-M), et la comparaison avec des heuristiques (genetique, greedy Sharpe) sur le S&P 500 ou le CAC 40. Au-dela du modele classique, les etudiants devront ajouter des contraintes realistes : lots entiers (100 actions par ligne), buy-in thresholds (`w_i = 0` ou `w_i >= w_min`), plafonds sectoriels, et limite de turnover au rebalancement.

### Objectifs
- Modeliser le probleme Sparse Markowitz avec cardinalite exacte K, lots entiers, et buy-in thresholds en CP-SAT (OR-Tools) et MILP (SCIP/Gurobi)
- Linearisation de la variance quadratique via factorisation de Cholesky ou approximation SOS
- Benchmarker CP-SAT, MILP, algo genetique (DEAP, PyGAD) sur front de Pareto risk-return (5 instances : 50, 100, 200, 500, 1000 actifs)
- Analyser l'impact des symmetry breakings (ordre lexicographique sur les titres selectionnes)
- Valider en Out-of-Sample sur 3 periodes distinctes via backtest QuantConnect Lean (Universe S&P 500, rebalance mensuel, commission realiste)

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Knapsack, cardinalite |
| App-10 Portfolio | [Search/Applications/Hybrid/App-10-Portfolio.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Applications/Hybrid/App-10-Portfolio.ipynb) | Baseline Markowitz + GA |
| QC-Py-10 Risk Portfolio | [QuantConnect/Python/QC-Py-10-Risk-Portfolio-Management.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/QuantConnect/Python/QC-Py-10-Risk-Portfolio-Management.ipynb) | Sizing, Kelly, stop-loss |
| QC-Py-14 Portfolio Construction | [QuantConnect/Python/QC-Py-14-Portfolio-Construction-Execution.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/QuantConnect/Python/QC-Py-14-Portfolio-Construction-Execution.ipynb) | Rebalance Lean framework |
| QC-Py-21 Portfolio-Optimization-ML | [QuantConnect/Python/QC-Py-21-Portfolio-Optimization-ML.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/QuantConnect/Python/QC-Py-21-Portfolio-Optimization-ML.ipynb) | ML + optimisation |

### References externes
- Markowitz, H. (1952). "Portfolio Selection." *Journal of Finance*, 7(1), 77-91. [JSTOR](https://www.jstor.org/stable/2975974)
- Bertsimas, D. & Shioda, R. (2009). "Algorithm for cardinality-constrained quadratic optimization." *Computational Optimization and Applications*, 43(1), 1-25. [Springer](https://link.springer.com/article/10.1007/s10589-007-9123-2)
- Bonami, P., Lodi, A., Tramontani, A., Wiese, S. (2018). "On mathematical programming with indicator constraints." *Annals of OR*. [Springer](https://link.springer.com/article/10.1007/s10479-017-2447-x)
- skfolio. "Mixed-Integer Cardinality Constraints." [skfolio.org](https://skfolio.org/auto_examples/mean_risk/plot_15_mip_cardinality_constraints.html)
- Cornuejols, G., & Tutuncu, R. (2006). "Optimization Methods in Finance." Cambridge. [CMU](http://web.math.ku.dk/~rolf/CT_FinOpt.pdf)
- OR-Tools CP-SAT Guide. [developers.google.com](https://developers.google.com/optimization/cp/cp_solver)

### Difficulte : 3/5

---

## M2 - Replication d'indice sous contraintes (Sparse Index Tracking)

La replication d'un ETF (SPY, CAC40, EuroStoxx) avec un nombre reduit K << N de titres est un probleme central de la gestion passive. Formellement, on cherche un portefeuille sparse `w` qui minimise la **tracking error** `|| R_p - R_benchmark ||` sur une fenetre historique, sous contraintes de cardinalite, de lots entiers, de sector caps, et de turnover au rebalancement periodique. Contrairement au Sparse Markowitz (M1) qui optimise un objectif risk-return, l'Index Tracking optimise une distance au benchmark : la formulation differe (L1 ou L2 tracking error, objectif lineaire ou quadratique). Les etudiants comparent MILP classique (Bertsimas 2015), CP-SAT avec `Element constraint`, et regression Lasso (baseline ML) sur 3 indices differents et 2 horizons (1 an, 5 ans). La validation se fait via backtest Lean avec benchmark = SPY et mesure du tracking error realise.

### Objectifs
- Formaliser la tracking error L1 et L2, et son equivalent integer lot (nombre d'actions au lieu de poids reels)
- Modeliser le probleme en CP-SAT avec cardinalite K ∈ {20, 30, 50}, sector caps, lots de 100 actions, et turnover cap
- Comparer au MILP classique (Gurobi, SCIP) et a la baseline Lasso (scikit-learn)
- Analyser l'impact du K sur la tracking error out-of-sample (bias/variance tradeoff)
- Backtest QuantConnect Lean : S&P 500 tracke par 30 actions, rebalance trimestriel 2019-2024, mesure tracking error realisee vs SPY

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Cardinalite, Knapsack |
| Search-9 Linear Programming | [Search/Part1-Foundations/Search-9-LinearProgramming.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-9-LinearProgramming.ipynb) | Simplex, LP |
| QC-Py-05 Universe Selection | [QuantConnect/Python/QC-Py-05-Universe-Selection.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/QuantConnect/Python/QC-Py-05-Universe-Selection.ipynb) | Manual universe, S&P 500 |
| QC-Py-14 Portfolio Construction | [QuantConnect/Python/QC-Py-14-Portfolio-Construction-Execution.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/QuantConnect/Python/QC-Py-14-Portfolio-Construction-Execution.ipynb) | Rebalance, execution |

### References externes
- Takeda, A., Niranjan, M., Gotoh, J., Kawahara, Y. (2015). "Simultaneous pursuit of out-of-sample performance and sparsity in index tracking portfolios." *arxiv:1506.05866*. [arXiv](https://arxiv.org/abs/1506.05866)
- Benidis, K., Feng, Y., Palomar, D. (2018). "Sparse Portfolios for High-Dimensional Financial Index Tracking." *arxiv:1809.01989*. [arXiv](https://arxiv.org/abs/1809.01989)
- Scozzari, A., Tardella, F., Paterlini, S., Krink, T. (2013). "Exact and heuristic approaches for the index tracking problem with UCITS constraints." *Annals of OR*. [Springer](https://link.springer.com/article/10.1007/s10479-012-1098-1)
- Rosenberg, G., et al. (2016). "Solving the Optimal Trading Trajectory Problem Using a Quantum Annealer." *arxiv:1508.06182*. [arXiv](https://arxiv.org/abs/1508.06182)
- Cornuejols, G., & Tutuncu, R. (2006). "Optimization Methods in Finance." Cambridge.

### Difficulte : 3/5

---

## M3 - Selection de paires pour stat-arb par enumeration de cliques (CP)

Le **statistical arbitrage par paires** (Gatev et al. 2006) consiste a trader des paires de titres cointegres : long l'un / short l'autre quand le spread s'ecarte de sa moyenne. Avec N=500 titres, il existe C(500,2)=124750 paires candidates ; apres filtre de cointegration (p-value < 0.05) on obtient typiquement quelques centaines d'edges dans un graphe. Le probleme combinatoire est : **selectionner un ensemble de K paires mutuellement disjointes** (chaque ticker dans au plus une paire) qui maximise le Sharpe esperé in-sample, sous contraintes de diversification sectorielle et de hedge-ratios entiers. C'est un probleme de **maximum weighted matching avec contraintes additionnelles**, qui se modelise nativement en CP-SAT avec `AtMostOne` par sommet et objectif lineaire pondere. Les etudiants comparent CP-SAT, MILP, et algorithmes de graphes classiques (Blossom de Edmonds) sur des donnees reelles US Equity.

### Objectifs
- Construire le graphe de cointegration : tester toutes les paires avec `statsmodels.tsa.stattools.coint`, filtrer a p < 0.05, ponderer par Sharpe in-sample
- Modeliser le probleme de matching avec contraintes en CP-SAT : `AtMostOne(x_{ij} for j)` pour chaque ticker i, objectif `max sum(sharpe_{ij} * x_{ij})`
- Comparer a MILP (Gurobi), a Blossom (networkx `max_weight_matching`), et une heuristique gloutonne
- Etudier l'impact de K (20, 50, 100 paires) et des contraintes sectorielles sur le Sharpe realise
- Backtest Lean : strategie long/short Z-score sur les paires retenues, commission realiste, 2019-2024

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-1 Fondamentaux | [Search/Part2-CSP/CSP-1-Fundamentals.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-1-Fundamentals.ipynb) | Modelisation CSP |
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Matching, optimisation |
| QC-Py-08 Multi-Asset | [QuantConnect/Python/QC-Py-08-Multi-Asset-Strategies.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/QuantConnect/Python/QC-Py-08-Multi-Asset-Strategies.ipynb) | Pairs, correlations |
| QC-Py-13 Alpha Models | [QuantConnect/Python/QC-Py-13-Alpha-Models.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/QuantConnect/Python/QC-Py-13-Alpha-Models.ipynb) | Alpha frameworks |

### References externes
- Gatev, E., Goetzmann, W.N., Rouwenhorst, K.G. (2006). "Pairs Trading: Performance of a Relative-Value Arbitrage Rule." *Rev. Fin. Studies*, 19(3). [Oxford](https://academic.oup.com/rfs/article/19/3/797/1593737)
- Caldeira, J., Moura, G. (2013). "Selection of a Portfolio of Pairs Based on Cointegration." *Brazilian Review of Finance*. [RePEc](https://ideas.repec.org/a/brf/journl/v11y2013i1p49-80.html)
- Korniejczuk, A. & Slepaczuk, R. (2024). "Statistical arbitrage in multi-pair trading strategy based on graph clustering algorithms in US equities market." *arxiv:2406.10695*. [arXiv](https://arxiv.org/abs/2406.10695)
- Edmonds, J. (1965). "Paths, Trees, and Flowers." *Canadian J. Math*, 17, 449-467. [Cambridge](https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/paths-trees-and-flowers/08B492B72322C4130AE800C0610E0E21)
- QuantConnect. "Pairs Trading Tutorial." [quantconnect.com](https://www.quantconnect.com/learning/articles/introduction-to-options/pairs-trading)

### Difficulte : 4/5

---

## M4 - Execution optimale d'ordres (TWAP/VWAP avec impact de marche)

L'**execution optimale** (Almgren-Chriss 2000) consiste a fractionner un grand ordre (p.ex. acheter 1M actions AAPL) sur un horizon H (30 minutes, 1 jour) de maniere a minimiser le **cout total** = impact permanent + impact temporaire + variance d'execution. La version continue se resout analytiquement, mais la version **discrete** avec quantites entieres, participation rate max (10% d'ADV par slot), lots minimums, et contraintes d'ordre (on ne peut pas depasser sa taille cible) est NP-difficile et se modelise en CP-SAT avec `IntervalVar` et `Cumulative`. Les etudiants comparent la solution optimale continue (formule fermee Almgren-Chriss), la version CP-SAT discrete, un simulated annealing, et valide sur des donnees minute de QuantConnect. L'aspect combinatoire est crucial pour les marches illiquides (smallcaps, crypto).

### Objectifs
- Implementer la formule fermee Almgren-Chriss et verifier numeriquement qu'elle donne bien une trajectoire deterministe
- Modeliser la version discrete en CP-SAT : variables entieres par slot, contrainte cumulative sur participation rate, contrainte d'integrite totale
- Calibrer les parametres d'impact (permanent λ, temporaire η) sur donnees minute via regression (Obizhaeva-Wang 2013)
- Comparer la qualite d'execution CP-SAT vs SA vs Almgren-Chriss continue sur 5 tickers (liquide + illiquide)
- Backtest Lean : strategie qui genere des gros ordres (rebalance portfolio) et les execute via schedule CP ; comparer cost of execution vs Market-on-open naive

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-4 Scheduling | [Search/Part2-CSP/CSP-4-Scheduling.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-4-Scheduling.ipynb) | IntervalVar, Cumulative |
| App-4 Job-Shop Scheduling | [Search/Applications/CSP/App-4-JobShopScheduling.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Applications/CSP/App-4-JobShopScheduling.ipynb) | Scheduling discret |
| QC-Py-09 Order Types | [QuantConnect/Python/QC-Py-09-Order-Types.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/QuantConnect/Python/QC-Py-09-Order-Types.ipynb) | Orders, execution |
| QC-Py-14 Portfolio Construction | [QuantConnect/Python/QC-Py-14-Portfolio-Construction-Execution.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/QuantConnect/Python/QC-Py-14-Portfolio-Construction-Execution.ipynb) | Execution models |

### References externes
- Almgren, R., Chriss, N. (2000). "Optimal Execution of Portfolio Transactions." *J. Risk*, 3(2), 5-39. [math.nyu.edu](https://www.math.nyu.edu/~almgren/papers/optliq.pdf)
- Obizhaeva, A., Wang, J. (2013). "Optimal Trading Strategy and Supply/Demand Dynamics." *J. Fin. Markets*, 16(1). [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1386418112000328)
- Busseti, E., Boyd, S. (2015). "Volume Weighted Average Price Optimal Execution." *Stanford*. [Stanford](https://web.stanford.edu/~boyd/papers/pdf/vwap_opt_exec.pdf)
- Rosenberg, G., et al. (2016). "Solving the Optimal Trading Trajectory Problem Using a Quantum Annealer." *arxiv:1508.06182*. [arXiv](https://arxiv.org/abs/1508.06182)
- Cartea, A., Jaimungal, S., Penalva, J. (2015). "Algorithmic and High-Frequency Trading." Cambridge UP. [CUP](https://www.cambridge.org/core/books/algorithmic-and-highfrequency-trading/56AC5C3F20B7CD08D5A14D4D04089C75)

### Difficulte : 4/5

---

## M5 - Allocation Risk-Parity sous contraintes de cardinalite

La strategie **Risk Parity** (ou Equal Risk Contribution, ERC, Maillard 2010) egalise la contribution au risque de chaque actif `σ_i * w_i * (Σw)_i = c` pour tout i. C'est une alternative populaire au Markowitz (1/N weighting ameliore) utilisee par Bridgewater (All Weather). La version **classique** se resout par optimisation convexe sans contrainte de cardinalite. La version **cardinalite K**, utile quand on veut allouer sur peu de titres (strategie simple, bas cout), devient non-convexe et NP-difficile : c'est un QCQIP (Quadratic Constrained Quadratic Integer Program) rarement etudie. Anis & Kwon (2022) proposent une formulation MIQCP recente que les etudiants doivent comparer a une approche CP-SAT avec linearisation.

### Objectifs
- Formaliser la condition ERC et sa variante cardinalite K
- Implementer la version classique (convexe) en cvxpy pour baseline
- Modeliser la version cardinalite en MIQCP (Gurobi) et en CP-SAT (avec linearisation de la contrainte quadratique)
- Analyser empiriquement : diversification effective (Effective Number of Bets), comparaison vs Sparse Markowitz (M1) et 1/K naif
- Backtest Lean : allocation ERC sur 10 ETFs sectoriels (XLK, XLF, ...), rebalance mensuel, covariance rolling 252 jours

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| App-10 Portfolio | [Search/Applications/Hybrid/App-10-Portfolio.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Applications/Hybrid/App-10-Portfolio.ipynb) | Markowitz baseline |
| CSP-5 Optimization | [Search/Part2-CSP/CSP-5-Optimization.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb) | Cardinalite |
| QC-Py-10 Risk-Portfolio | [QuantConnect/Python/QC-Py-10-Risk-Portfolio-Management.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/QuantConnect/Python/QC-Py-10-Risk-Portfolio-Management.ipynb) | Risk sizing |
| QC-Py-21 Portfolio-Optimization-ML | [QuantConnect/Python/QC-Py-21-Portfolio-Optimization-ML.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/QuantConnect/Python/QC-Py-21-Portfolio-Optimization-ML.ipynb) | ML + optimisation |

### References externes
- Maillard, S., Roncalli, T., Teiletche, J. (2010). "The Properties of Equally Weighted Risk Contribution Portfolios." *JPM*, 36(4). [IIJ](https://jpm.pm-research.com/content/36/4/60)
- Anis, H., Kwon, R. (2022). "Cardinality-constrained risk parity portfolios." *EJOR*, 302(1), 392-414. [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0377221721011012)
- Cesarone, F., Tardella, F. (2017). "Equal Risk Bounding is better than Risk Parity for Portfolio Selection." *J. Global Optim*, 68(2). [Springer](https://link.springer.com/article/10.1007/s10898-016-0477-6)
- Roncalli, T. (2013). "Introduction to Risk Parity and Budgeting." CRC Press. [Routledge](https://www.routledge.com/Introduction-to-Risk-Parity-and-Budgeting/Roncalli/p/book/9781482207156)

### Difficulte : 4/5

---

## M6 - Arbitrage triangulaire crypto par detection de cycles (CP + Bellman-Ford)

Sur un exchange crypto (Binance, Kraken), 8 cryptos majeurs (BTC, ETH, BNB, USDT, USDC, SOL, ADA, XRP) forment un graphe complet de 28 paires de trading. Une opportunite d'**arbitrage triangulaire** (ou quadrilateral, jusqu'a 5 sauts) consiste en un cycle de conversions `A -> B -> C -> A` avec un profit net positif apres frais. Detecter un tel cycle = trouver un cycle negatif dans le graphe log-pondere (Bellman-Ford) ; mais la version **realiste** ajoute des contraintes : frais maker/taker 0.1%, slippage en fonction du depth-of-book, taille minimale d'ordre, contrainte d'execution simultanee (latence). Cela transforme la detection en probleme CP avec contraintes non triviales. Les etudiants comparent Bellman-Ford naïf vs CP-SAT avec `Circuit constraint` et contraintes supplementaires, sur un flux de marche Binance (WebSocket).

### Objectifs
- Implementer le pipeline de detection : flux orderbook Binance (WebSocket via `python-binance`), construction du graphe log-spread, detection cycles negatifs
- Comparer 3 approches : Bellman-Ford classique, CP-SAT avec `Circuit`, heuristique greedy DFS
- Ajouter les contraintes realistes : frais, slippage depth-based, tailles min d'ordre, rentabilite nette > threshold
- Analyser la frequence d'apparition des opportunites en fonction du seuil de rentabilite net et de la profondeur de cycle (3-5 sauts)
- Integration QuantConnect : implementer une strategie "monitoring only" qui detecte et logue les opportunites (sans exec reelle, car la latence depasse les capacites Lean) ; alternative : simulation batch sur historique Binance

### Notebooks CoursIA pertinents

| Notebook | Chemin | Pertinence |
|----------|--------|------------|
| CSP-1 Fondamentaux | [Search/Part2-CSP/CSP-1-Fundamentals.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-1-Fundamentals.ipynb) | Modelisation CSP |
| App-13 TSP | [Search/Applications/Hybrid/App-13-TSP-Metaheuristics.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Applications/Hybrid/App-13-TSP-Metaheuristics.ipynb) | Cycles, Circuit constraint |
| QC-Py-07 Futures/Forex | [QuantConnect/Python/QC-Py-07-Futures-Forex.ipynb](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/QuantConnect/Python/QC-Py-07-Futures-Forex.ipynb) | Crypto feeds, leverage |

### References externes
- Xu, Y., Livshits, B. (2019). "The anatomy of a cryptocurrency pumping-and-dumping scheme." *USENIX Security*. [USENIX](https://www.usenix.org/conference/usenixsecurity19/presentation/xu-yiming)
- Makarov, I. & Schoar, A. (2020). "Trading and Arbitrage in Cryptocurrency Markets." *Journal of Financial Economics*, 135(2), 293-319. [ScienceDirect](https://doi.org/10.1016/j.jfineco.2019.07.001)
- Angeris, G., Chitra, T. (2020). "Improved Price Oracles: Constant Function Market Makers." *AFT'20*. [arXiv](https://arxiv.org/abs/2003.10001)
- Bellman, R. (1958). "On a routing problem." *Quarterly of Applied Math*, 16(1). [AMS](https://www.ams.org/journals/qam/1958-16-01/S0033-569X-1958-0102435-2/)
- Binance API Docs. [binance-docs.github.io](https://binance-docs.github.io/apidocs/spot/en/)

### Difficulte : 3/5

---

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

*Derniere mise a jour : Avril 2026*
*Contact : Equipe pedagogique Programmation par Contraintes, EPITA SCIA*
