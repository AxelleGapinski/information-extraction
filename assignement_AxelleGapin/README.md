# Pipeline d'analyse de diagnostics immobiliers

## Description du projet
Ce projet vise à développer une pipeline d'analyse automatisée de rapports de diagnostics immobiliers. L'objectif est de transformer des rapports non structurés en données exploitables et synthétiques pour les professionnels de l'immobilier et les acheteurs potentiels.
Les diagnostics sont des documents PDF qui contiennent des informations sur l'état du bien immobilier (état de l'amiante, de l'électricité, etc.). Ces informations sont essentielles pour évaluer l'état du bien et les travaux à réaliser.

## Structure du projet
- `/data` - Dossier contenant les dossiers des rapports à analyser
  - Chaque dossier contient des fichiers PDF de diagnostics immobiliers (.pdf) ainsi que leur texte extrait (.txt)
- `/prompts` - Dossier contenant les prompts pour le traitement des données
- `/steps` - Dossier contenant les étapes de traitement des données 
- `/outputs` - Résultats des analyses
- `runner.py` - Runner qui lance les étapes de traitement dans l'ordre
- `main.py` - Fichier principal pour lancer l'analyse
  - Tu dois rajouter les nouveaux steps dans le runner pour les exécuter.

## Étapes de la Pipeline
- 'steps\read_files.py': lecture des fichiers
- 'steps\extract_info.py' : extractions des informations, utilisation de l'API OpenAI pour structurer les données
- 'steps\synthese_export.py': synthèse globale: génération d'une synthèse avec des points critiques
- 'steps\synthese_export.py': Exportt des données: création de fichiers CSV et txt


## Prérequis
- Python 3.8+
- Accès à l'API OpenAI

## Utilisation
1. Installer les dépendances requises en exécutant `pip install -r requirements.txt`
2. Configurer les variables d'environnement (`OpenAI`)
3. Lancer le script `main.py` pour lancer l'analyse sur un dossier
