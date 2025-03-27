# Gestion Scolaire API

Une API RESTful pour la gestion des salles de classe, cours et filières dans un établissement scolaire.

## Fonctionnalités

- Gestion des salles (création, modification, suppression)
- Gestion des cours (création, modification, suppression)
- Gestion des filières (création, modification, suppression)
- Gestion des classes (création, modification, suppression)
- Authentification JWT
- Assignation des salles aux classes

## Installation

1. Cloner le dépôt :
```bash
git clone https://github.com/parfait2001/tpaqlapi.git
cd tpaqlapi

## Créer un environnement virtuel :

python -m venv venv
source venv/bin/activate  # Sur Linux/Mac
venv\Scripts\activate     # Sur Windows

## Installer les dépendances :

pip install -r requirements.txt
pip install -r dev-requirements.txt  # Pour le développement
Configurer l'environnement :


## Créer un fichier config.py à la racine avec :

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/tpaql_db' # Pour Mysql
    DATABASE_URL=postgresql://user:password@localhost/dbname  # Pour postgresql
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'votre-secret-key'

Générer la clé avec le fichier key.py en l'executant tout simplement

## Initialiser la base de données :
flask db init
flask db migrate
flask db upgrade
Utilisation

## Démarrer le serveur :

flask run