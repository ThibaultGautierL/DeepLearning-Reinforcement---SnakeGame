Snake AI - Deep Learning avec PyTorch
=====================================

Table des matières
------------------
1. À propos
2. Prérequis
3. Domaine du problème
4. Exécution
5. Résultats
6. Conclusion
7. Licence

---

1. À propos
-----------
Ce projet vise à développer un agent basé sur le deep learning, entraîné avec PyTorch, pour jouer au célèbre jeu Snake.  
L'objectif est d'utiliser des techniques simples d'apprentissage par renforcement pour entraîner un réseau de neurones à maximiser son score en collectant des pommes et en évitant les collisions.

Ce projet est conçu pour les débutants qui souhaitent comprendre les bases de l'apprentissage par renforcement, tout en travaillant sur un projet ludique.

---

2. Prérequis
------------
Aucun prérequis spécifique pour le système d'exploitation ou la version de Python.  

### Dépendances Python :
Les dépendances nécessaires sont les suivantes, vous pouvez les installer directement avec `pip install` :
- torch
- pygame
- numpy

---

3. Domaine du problème
-----------------------
Le problème est modélisé comme suit :

- **États :** Le Snake est représenté par 11 variables binaires décrivant son environnement, notamment :
  - Danger devant, à gauche, à droite.
  - Direction actuelle (haut, bas, gauche, droite).
  - Position relative de la pomme (haut, bas, gauche, droite).
  
- **Actions :** L'agent peut effectuer trois actions possibles :
  1. Aller tout droit.
  2. Tourner à gauche.
  3. Tourner à droite.

- **Récompenses :**
  - **+10** : Lorsqu'une pomme est mangée.
  - **-10** : Lorsque l'agent perd (collision avec lui-même ou un mur).
  - **-1** : À chaque pas, pour inciter à terminer plus rapidement.

L'architecture du modèle est un réseau neuronal simple avec une couche cachée :
- **Entrées :** 11 (les variables d'état).
- **Couche cachée :** 256 neurones.
- **Sorties :** 3 (correspondant aux actions possibles).

---

4. Exécution
------------
### Étape 1 : Cloner le dépôt
git clone <URL_DU_DEPOT>
cd <NOM_DU_PROJET>


### Étape 2 : Installer les dépendances  
Installez les dépendances nécessaires.

### Étape 3 : Lancer l'entraînement  
Pour démarrer l'entraînement, exécutez le fichier `agent.py` :  
python agent.py  

L'entraînement sauvegardera le modèle entraîné dans un fichier `model/model.pth`.

---

5. Résultats
------------
Après environ 1000 parties, l'agent atteint un score moyen de 20-25 pommes.  
Cependant, l'agent présente encore des limitations :  
- Il peut se heurter à son propre corps dans certaines situations.
- L'optimisation des hyperparamètres et des récompenses pourrait améliorer ses performances.

---

6. Conclusion
-------------
Ce projet démontre comment un réseau neuronal simple peut être utilisé pour résoudre des problèmes classiques comme Snake. Bien qu'il atteigne des résultats acceptables, il existe des pistes d'amélioration, telles que :
- L'utilisation de techniques plus avancées, comme DQN (Deep Q-Networks) ou des CNN pour une meilleure représentation visuelle.
- Des ajustements du système de récompenses pour encourager un comportement plus optimal.

---

7. Licence
----------
Ce projet est basé sur le code de Patrick Loeber et est distribué sous licence MIT.  
