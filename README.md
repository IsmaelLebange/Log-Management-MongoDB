# Administration MongoDB pour la gestion de données non structurées

## Gestion de logs issus d'un système e-learning

Ce projet porte sur l'**administration d'une base de données MongoDB destinée à la gestion de données non structurées**, dans le contexte d'un système e-learning.

Les données étudiées sont principalement des **logs d'activité des utilisateurs** d'une plateforme d'apprentissage en ligne. Le projet explore différentes techniques d'administration et d'optimisation de MongoDB afin de stocker, interroger et traiter efficacement ces données.

Les principales problématiques étudiées sont :

* la génération et l'importation des logs ;
* l'organisation et l'interrogation des données ;
* la création d'index ;
* les opérations d'agrégation ;
* l'agrégation hybride ;
* le partitionnement des données avec le sharding ;
* la distribution des données entre les shards ;
* la mesure des performances des opérations.

---

## 1. Contexte

Les plateformes e-learning génèrent de grandes quantités de données d'activité : connexions, consultations, interactions avec les ressources pédagogiques, actions des utilisateurs, etc.

Ces données de logs sont généralement **semi-structurées ou non structurées** et peuvent présenter des formats et des volumes variables.

MongoDB, en tant que système de gestion de bases de données orienté documents, constitue une solution adaptée à ce type de données.

L'objectif du projet est donc d'étudier l'administration d'un environnement MongoDB permettant de gérer ces logs et d'évaluer différentes stratégies d'accès et de distribution des données.

---

## 2. Objectifs

Le projet vise notamment à :

1. Générer un ensemble de logs représentatifs d'une plateforme e-learning.
2. Importer ces données dans MongoDB.
3. Mettre en place des index adaptés aux requêtes étudiées.
4. Exécuter différentes requêtes sur les données.
5. Utiliser les pipelines d'agrégation MongoDB.
6. Étudier une approche d'agrégation hybride.
7. Mettre en place un environnement MongoDB distribué avec sharding.
8. Analyser la distribution des données entre les shards.
9. Mesurer les temps d'insertion et d'exécution des requêtes.
10. Comparer les performances obtenues selon les configurations étudiées.

---

## 3. Architecture du projet

Le projet est organisé en trois parties principales :

```text
src/
├── queries/
├── scripts/
└── results/
```

### `queries/`

Contient les scénarios de requêtes et les fichiers de configuration liés à l'environnement MongoDB.

```text
queries/
├── R1_actions_user.txt
├── R2_actions_user.txt
├── R3_actions_user.txt
└── mongod_shard2.conf
```

Les fichiers `R1_actions_user.txt`, `R2_actions_user.txt` et `R3_actions_user.txt` correspondent aux différents scénarios de requêtes utilisés pour l'expérimentation.

`mongod_shard2.conf` contient la configuration d'un serveur MongoDB participant à l'environnement de sharding.

---

## 4. Scripts d'administration et d'expérimentation

Le dossier `scripts/` regroupe les scripts permettant d'automatiser les différentes opérations réalisées sur MongoDB.

```text
scripts/
├── agregate_hybrid.py
├── create_indexes.py
├── create_indexes_agreg.py
├── generate_logs.py
├── import_logs.py
├── import_logs_agreg.py
├── run_queries.py
├── run_queries_agreg.py
├── shard_setup.js
├── test_mongo.py
└── utils.py
```

### Génération des données

`generate_logs.py` permet de générer les logs utilisés comme données expérimentales.

### Importation

Les scripts suivants permettent d'importer les données dans MongoDB :

```text
import_logs.py
import_logs_agreg.py
```

### Indexation

Les scripts :

```text
create_indexes.py
create_indexes_agreg.py
```

permettent de créer les index nécessaires aux différents scénarios d'exploitation des données.

### Requêtes

Les scripts :

```text
run_queries.py
run_queries_agreg.py
```

permettent d'exécuter les requêtes et d'effectuer les mesures associées.

### Agrégation hybride

`agregate_hybrid.py` est utilisé pour l'expérimentation portant sur l'agrégation hybride.

### Sharding

`shard_setup.js` permet de mettre en place et de configurer l'environnement de sharding MongoDB.

### Tests

`test_mongo.py` permet de vérifier le fonctionnement de l'environnement MongoDB.

### Utilitaires

`utils.py` regroupe les fonctions communes utilisées par les différents scripts.

---

## 5. Indexation

L'indexation constitue un élément important de l'administration de la base.

Des index sont créés afin d'améliorer les performances des requêtes exécutées sur les logs.

Deux scripts sont notamment utilisés :

```text
create_indexes.py
create_indexes_agreg.py
```

Le second scénario est destiné aux opérations faisant intervenir les traitements d'agrégation.

L'objectif est d'observer l'influence de l'indexation sur les temps d'exécution des opérations.

---

## 6. Agrégation

MongoDB fournit un framework d'agrégation permettant de traiter et d'analyser les documents stockés dans la base.

Le projet étudie différentes opérations d'agrégation à travers notamment :

```text
agregate_hybrid.py
import_logs_agreg.py
run_queries_agreg.py
create_indexes_agreg.py
```

L'objectif est d'exploiter les données de logs afin d'obtenir des informations utiles à partir des activités enregistrées par la plateforme e-learning.

---

## 7. Sharding

Afin d'étudier la gestion distribuée des données, le projet met également en œuvre le **sharding MongoDB**.

Le sharding permet de répartir les données sur plusieurs serveurs MongoDB.

Les principaux fichiers associés sont :

```text
mongod_shard2.conf
shard_setup.js
```

Cette partie permet d'étudier :

* la configuration d'un environnement distribué ;
* la répartition des données ;
* l'impact du sharding sur l'accès aux données ;
* la distribution des données entre les shards.

---

## 8. Évaluation des performances

Les résultats expérimentaux sont stockés dans le dossier `results/` :

```text
results/
├── insert_times.csv
├── query_times.csv
└── shard_distribution.csv
```

### `insert_times.csv`

Contient les mesures relatives aux temps d'insertion des données.

### `query_times.csv`

Contient les mesures relatives à l'exécution des différents scénarios de requêtes.

### `shard_distribution.csv`

Permet d'analyser la distribution des données entre les différents shards.

Ces mesures permettent d'évaluer les choix d'administration et d'optimisation effectués durant l'expérimentation.

---

## 9. Workflow

Le fonctionnement général du projet peut être résumé ainsi :

```text
Génération des logs e-learning
            |
            v
       Import MongoDB
            |
            v
   Administration / Indexation
            |
       +----+----+
       |         |
       v         v
   Requêtes   Agrégation
       |         |
       +----+----+
            |
            v
         Sharding
            |
            v
    Mesure des performances
            |
            v
       Résultats CSV
```

---

## 10. Technologies

* **MongoDB** : système de gestion de base de données orienté documents.
* **Python** : génération des données, administration et expérimentation.
* **PyMongo** : interaction avec MongoDB depuis Python.
* **JavaScript** : configuration du sharding.
* **MongoDB Indexes** : optimisation des requêtes.
* **MongoDB Aggregation Framework** : traitement et analyse des données.
* **MongoDB Sharding** : distribution des données.
* **CSV** : stockage des résultats expérimentaux.

---

## 11. Structure complète

```text
Log-Management-MongoDB/
│
├── src/
│   ├── queries/
│   │   ├── R1_actions_user.txt
│   │   ├── R2_actions_user.txt
│   │   ├── R3_actions_user.txt
│   │   └── mongod_shard2.conf
│   │
│   ├── scripts/
│   │   ├── agregate_hybrid.py
│   │   ├── create_indexes.py
│   │   ├── create_indexes_agreg.py
│   │   ├── generate_logs.py
│   │   ├── import_logs.py
│   │   ├── import_logs_agreg.py
│   │   ├── run_queries.py
│   │   ├── run_queries_agreg.py
│   │   ├── shard_setup.js
│   │   ├── test_mongo.py
│   │   └── utils.py
│   │
│   └── results/
│       ├── insert_times.csv
│       ├── query_times.csv
│       └── shard_distribution.csv
│
└── README.md
```

---

## 12. Auteur

**Ismael Lebange**

Projet académique d'administration de bases de données consacré à l'utilisation de MongoDB pour la gestion et l'exploitation de données de logs issues d'un système e-learning.
# Implémentation de la gestion des logs avec MongoDB
