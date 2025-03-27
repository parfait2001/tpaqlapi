```markdown
# 🚀 API de Gestion de Réservation de Salles

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-production-ready-brightgreen)

## ✨ Fonctionnalités

**Gestion des salles**  
✅ Création, modification, suppression  
✅ Consultation des disponibilités  
✅ Historique des réservations  

**Gestion académique**  
📚 Création et gestion des cours  
🎓 Gestion des filières  
🏫 Gestion des classes  

**Sécurité**  
🔒 Authentification JWT  
👨‍💼 Rôles et permissions  
🛡️ Protection des endpoints  

**Réservations**  
⏱️ Assignation des salles aux classes  
🗓️ Gestion des créneaux horaires  
⚠️ Prévention des conflits de réservation  

## 🛠️ Installation

### Prérequis
- Python 3.9+
- MySQL ou PostgreSQL
- Git

### 1. Clonage du dépôt
```bash
git clone https://github.com/parfait2001/tpaqlapi.git
cd tpaqlapi
```

### 2. Configuration de l'environnement
```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Installation des dépendances
```bash
pip install -r requirements.txt

# Pour le développement
pip install -r dev-requirements.txt
```

### 3. Configuration de l'application
Créez `config.py`:

```python
class Config:
    # MySQL (par défaut)
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/tpaql_db'
    
    # PostgreSQL (alternative)
    # SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/dbname'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'votre-secret-key-tres-securise'
```

Générez une clé JWT:
```bash
python key.py
```

### 4. Base de données
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## 🏃‍♂️ Utilisation

Démarrer le serveur:
```bash
flask run
```

Accédez à: `http://localhost:5000`

**Variables d'environnement:**
| Variable | Valeur par défaut | Description |
|----------|------------------|-------------|
| FLASK_APP | app.py | Fichier principal |
| FLASK_ENV | development | Mode d'exécution |
| FLASK_DEBUG | 1 | Mode debug |

