# Application Médicale FastAPI

Ce projet est une application médicale construite avec FastAPI.

## Démarrage rapide (Docker Compose)

Si Docker Desktop est installé et démarré, lance directement:

```bash
docker compose up --build
```

Accès: http://127.0.0.1:8000 et http://127.0.0.1:8000/docs

Pour arrêter:

```bash
docker compose down
```

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

## Utiliser PostgreSQL (développement)

Par défaut l'application peut fonctionner en mémoire, mais pour la persistance vous pouvez configurer PostgreSQL :

1. Créez une base PostgreSQL (ex: `medbridge`) et un utilisateur avec mot de passe.
2. Copiez `.env.example` en `.env` et modifiez `DATABASE_URL` (format async pour SQLAlchemy + asyncpg) :

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/medbridge
```

Si vous utilisez `docker compose` fourni (service `db`), vous pouvez utiliser :

```env
DATABASE_URL=postgresql+asyncpg://medbridge:medbridge123@db:5432/medbridge_db
```

3. Installez les dépendances et créez les tables :

```bash
pip install -r requirements.txt
python create_tables.py
```

4. Lancez le serveur :

```bash
uvicorn main:app --reload
```

Note: Pour des migrations structurées, vous pouvez initialiser Alembic (`alembic init alembic`) et créer une première révision; j'ai ajouté `alembic` aux dépendances pour faciliter la suite.

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