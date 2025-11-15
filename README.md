# Application Médicale FastAPI

Ce projet est une application médicale construite avec FastAPI.

## Prérequis

- Python 3.12 ou supérieur
- Un environnement virtuel Python (venv)

## Installation

1. Cloner le repository :
```bash
git clone https://github.com/NO-YA/MedBridge.git
cd MedBridge
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
pip install -r requirements.txt
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

## Exécution avec Docker

- Build de l'image
```bash
docker build -t medbridge-api .
```

- Lancer le conteneur
```bash
docker run -it --rm -p 8000:8000 medbridge-api
```

- Avec Docker Compose
```bash
docker compose up --build
docker compose down
```

## Développement

Le mode `--reload` est activé par défaut, ce qui signifie que le serveur se rechargera automatiquement à chaque modification du code.

## Arrêt du serveur

Pour arrêter le serveur, appuyez sur `Ctrl+C` dans le terminal.

## Structure du projet

```
MedBridge/
├── main.py               # Point d'entrée de l'application
├── requirements.txt      # Dépendances Python
├── Dockerfile            # Image Docker pour exécuter l'app
├── docker-compose.yml    # Lancement simplifié avec Docker Compose
├── .dockerignore         # Fichiers ignorés par Docker
├── .venv/                # (Optionnel) Environnement virtuel local
└── README.md             # Ce fichier