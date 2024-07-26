# Détection des Plaques d'Immatriculation

## Introduction

Ce projet utilise FastAPI pour créer une API permettant de détecter et générer des plaques d'immatriculation.

## Installation

1. Clonez le dépôt.
2. creer un environnement virtuelle `pip install -r requirements.txt`
3. lancer l'environnemet virtuel 
`source env/bin/activate  # Pour Linux/Mac
 iaenv\Scripts\activate     # Pour Windows`
4. Installez les dépendances avec `pip install -r requirements.txt`.

## Utilisation

1. Lancer l'API avec `uvicorn app.main:app --reload`.
2. Accédez à `http://127.0.0.1:8000` pour utiliser l'interface web.


## Structure du Projet

- `app/` : Contient les fichiers principaux de l'application FastAPI.
- `data/` : Contient les données brutes et préparées.
- `models/` : Contient les scripts d'entraînement des modèles.
- `scripts/` : Contient les scripts pour collecter et préparer les données.
- `requirements.txt` : Liste des dépendances.
- `README.md` : Documentation du projet.
