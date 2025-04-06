# MaxPar – Parallélisation maximale automatique

**MaxPar** est une librairie Python développée pour optimiser l'exécution de systèmes de tâches en automatisant leur parallélisation maximale. Cette solution permet à l'utilisateur de spécifier des tâches interdépendantes et de gérer leur exécution tout en respectant les contraintes de précédence, garantissant ainsi une exécution correcte et ordonnée des tâches.

Le principal objectif de **MaxPar** est d'améliorer l'efficacité et la performance des traitements en exploitant au mieux les capacités de parallélisation des systèmes, tout en simplifiant la gestion des dépendances entre tâches. Grâce à une interface intuitive, cette librairie permet aux développeurs de tirer parti du parallélisme pour accélérer leurs processus tout en respectant les contraintes de précédence.

En outre, **MaxPar** utilise **Matplotlib** et **NetworkX** pour visualiser les dépendances entre les tâches sous forme de diagrammes, offrant ainsi une meilleure compréhension de l'ordonnancement des tâches et du parallélisme du système.

## Objectifs

- Développer une librairie permettant l’optimisation de l’exécution des systèmes de tâches par la parallélisation maximale.
- Offrir une solution intuitive permettant à l'utilisateur de spécifier des tâches interdépendantes et de gérer leur exécution tout en respectant les contraintes de précédence.
- Maximiser l’utilisation des ressources systèmes disponibles pour augmenter les performances des traitements parallèles.
- Garantir une exécution correcte et ordonnée des tâches tout en simplifiant la gestion des dépendances.
- Visualiser les dépendances des tâches sous forme de **graphes** avec **NetworkX** et **Matplotlib**.

## Fonctionnalités principales

- **Parallélisation maximale des tâches** : Exécution parallèle des tâches interdépendantes en exploitant au mieux les ressources système disponibles.
- **Gestion des dépendances** : Spécification facile des tâches interdépendantes avec respect des contraintes de précédence.
- **Exécution ordonnée** : Les tâches sont exécutées de manière correcte, respectant l'ordre des dépendances entre elles.
- **Visualisation des dépendances** : Utilisation de **NetworkX** pour générer un graphique des dépendances entre les tâches, et de **Matplotlib** pour afficher ce diagramme sous forme visuelle.
- **Facilité d'intégration** : Interface simple à intégrer dans des projets Python existants pour optimiser les performances de traitement.

## Technologies utilisées

Python, Concurrence, Modules standard (threading, multiprocessing), Matplotlib et NetworkX

## À propos

Ce projet a été développé en binôme dans le cadre de la L3 en Systèmes d'exploitation.
