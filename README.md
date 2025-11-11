# Application Médicale FastAPI

Ce projet est une application médicale construite avec FastAPI.

## Prérequis

- Python 3.14 ou supérieur
- Un environnement virtuel Python (venv)

## Installation

1. Cloner le repository :
```bash
git clone https://github.com/NO-YA/MedBridge.git
cd fastapi-todo
```

2. Créer un environnement virtuel :
```bash
python -m venv .venv
```

3. Activer l'environnement virtuel :

- Sous Windows (PowerShell) :
```powershell
.\.venv\Scripts\Activate.ps1
```

- Sous Windows (CMD) :
```cmd
.\.venv\Scripts\activate.bat
```

- Sous Linux/MacOS :
```bash
source .venv/bin/activate
```

4. Installer les dépendances :
```bash
pip install fastapi uvicorn
```

## Lancement de l'application

1. Activer l'environnement virtuel (voir étape 3 ci-dessus)

2. Lancer le serveur :
```bash
uvicorn main:app --reload
```

L'application sera accessible aux adresses suivantes :
- Interface principale : http://127.0.0.1:8000
- Documentation Swagger : http://127.0.0.1:8000/docs
- Documentation ReDoc : http://127.0.0.1:8000/redoc

## Développement

Le mode `--reload` est activé par défaut, ce qui signifie que le serveur se rechargera automatiquement à chaque modification du code.

## Arrêt du serveur

Pour arrêter le serveur, appuyez sur `Ctrl+C` dans le terminal.

## Structure du projet

```
fastapi-todo/
├── .venv/              # Environnement virtuel Python
├── main.py            # Point d'entrée de l'application
└── README.md         # Ce fichier
```

C:/Users/N.O.Y.A/Documents/fastapi-todo/.venv/Scripts/Activate.ps1; uvicorn main:app --reload