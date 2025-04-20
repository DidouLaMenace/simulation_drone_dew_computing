# Simulation de drone autonome avec Dew Computing

Ce projet simule un drone autonome chargé de détecter des victimes après une catastrophe naturelle.  
Le drone suit une trajectoire définie manuellement sur une carte interactive, traite les données localement (modèle Dew Computing), et détecte les victimes sur son trajet.

---

## Dépendances

Assurez-vous d'utiliser **Python 3.7+**.

Installez les bibliothèques nécessaires :

```bash
pip install flask flask-cors folium
```

## Arborescence du projet

.
├── carte_victimes_trajet.html #*Carte finale avec trajet + victimes détectées*
├── coordonnees_points.json  #*Coordonnées envoyées depuis la carte*
├── main_simulation.py #*Génère les victimes*
├── rapport #*Dossier contenant les rapports de mission (.txt)*
│   └── resume_mission_drone_2025-04-19_19-34-19.txt
├── selection_points.html #*Carte interactive pour choisir le trajet*
├── server.py  #*Serveur Flask pour recevoir les coordonnées*                                       
└── stockage_local.json #*Victimes détectées et stockées localement*


## Lancement de l'application

#### 1. Démarrer le serveur Flask
Dans un terminal (à la racine du projet) :

```bash
python3 server.py
```

Ce serveur attend les coordonnées envoyées par la carte.

#### 2. Lancer un serveur local pour la carte
Dans un autre terminal, lance le serveur HTTP :

```bash
python3 -m http.server 8000
```

#### 3. Ouvrir la carte interactive
Dans ton navigateur, va à :

```bash
http://localhost:8000/selection_points.html
```

Clique une fois pour choisir le point de départ (🔵)

Puis une deuxième fois pour le point d’arrivée (🟣)

Un message "Coordonnées enregistrées !" apparaîtra si tout fonctionne

#### 4. Lancer la simulation
Une fois les points choisis, exécute le script principal :

```bash
python3 main_simulation.py
```

Vous pouvez observer la détection de victimes en vous rendant à l'URL : 
```bash
http://localhost:8000/carte_victimes_trajet.html
```

Ce script :

- Génère des points simulés le long du trajet

- Détecte aléatoirement des victimes

- Stocke les victimes détectées dans *stockage_local.json*

- Génère une carte interactive *carte_victimes_trajet.html*

## Résultat
Ouvre *carte_victimes_trajet.html* dans ton navigateur pour visualiser :

- Le trajet du drone (ligne noire)

- Les victimes détectées (priorité critique, modérée, faible)

- Départ (bleu) / Arrivée (violet)


Un rapport texte est généré automatiquement dans le dossier rapport/, avec un nom horodaté : ````rapport/resume_mission_drone_2025-04-19_23-09-45.txt````

Le fichier contient :
- Un récapitulatif global (nombre de victimes par niveau)
- La position GPS de chaque victime triée par criticité