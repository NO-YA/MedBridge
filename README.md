# MedBridge — API To-Do médicale (FastAPI)

Petite API de gestion de tâches médicales construite avec FastAPI. Le projet utilise SQLite localement pour la persistance (via `sqlmodel`).

**Principales fonctionnalités**
- CRUD complet pour les tâches (`/todos/`)
- Documentation interactive : `/docs` (Swagger) et `/redoc`

## Démarrage rapide avec Docker Compose

Pour lancer l'application avec Docker Compose (recommandé):

```bash
git clone https://github.com/NO-YA/MedBridge.git
cd MedBridge
docker compose up --build
```

L'API sera accessible sur `http://localhost:8000/docs` (Swagger UI).

## Prérequis

1. Cloner le repository :
```bash
git clone https://github.com/NO-YA/MedBridge.git
cd MedBridge
```

# MedBridge — API To-Do médicale (FastAPI)

Petite API de gestion de tâches médicales construite avec FastAPI. Le projet utilise SQLite localement pour la persistance (via `sqlmodel`).

**Principales fonctionnalités**
- CRUD complet pour les tâches (`/todos/`)
- Documentation interactive : `/docs` (Swagger) et `/redoc`

## Prérequis

- Python 3.11+ (3.12 recommandé) — pour exécution locale
- Docker + Docker Compose — pour exécution en conteneur (recommandé)

## Installation et exécution (local)

1. Cloner le repository:

```bash
git clone https://github.com/NO-YA/MedBridge.git
cd MedBridge
```

2. Créer et activer un environnement virtuel:

Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux / macOS:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Installer les dépendances (versions pinées dans `requirements.txt`):

```bash
pip install -r requirements.txt
```

4. Lancer l'application en mode développement:

```bash
uvicorn main:app --reload
```

Accéder ensuite à:
- API root : `http://127.0.0.1:8000/`
- Swagger UI : `http://127.0.0.1:8000/docs`
- ReDoc : `http://127.0.0.1:8000/redoc`

## Configuration (variables d'environnement)

- `DATABASE_URL` : URL de la base de données SQLAlchemy. Par défaut: `sqlite:///./medbridge.db`.
	- Exemple pour un volume Docker : `sqlite:////data/medbridge.db` (notez les 4 slashs pour chemin absolu).

## Exécution avec Docker Compose (recommandé)

Lancer l'application complète avec persistance SQLite :

```bash
docker compose up --build
```

L'API sera disponible sur :
- Swagger UI : `http://localhost:8000/docs`
- ReDoc : `http://localhost:8000/redoc`
- API root : `http://localhost:8000/`

Pour arrêter :
```bash
docker compose down
```

> La base de données SQLite est stockée dans un volume Docker persistant (`medbridge-data`). Les données survivront aux redémarrages du conteneur.

## Tests et qualité

- Pour ajouter des tests : utiliser `pytest` + `httpx` (client de test). Exemple : `pytest tests/`.
- Linter / formatter recommandés : `ruff`, `black`, et `isort`.
- Audit de dépendances : `pip-audit` / `pip-audit`.

Exemples de commandes (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt pytest httpx pip-audit ruff black
ruff check .
black .
pip-audit
pytest
```

## Notes de déploiement

- Ne pas utiliser l'option `--reload` en production.
- Pour la production, exécuter l'app derrière un processus maître (ex: `gunicorn -k uvicorn.workers.UvicornWorker`) et utiliser PostgreSQL.
- Ajouter des migrations (Alembic) si vous migrez vers PostgreSQL.

## Prochaines améliorations proposées

- Ajouter tests unitaires et d'intégration CI (GitHub Actions)
- Ajouter authentification/autorisation (OAuth2/JWT) si l'application manipule des données patients
- Remplacer SQLite par PostgreSQL pour multi-instance et sauvegardes régulières

## Structure du projet

```
MedBridge/
├── main.py               # Point d'entrée de l'application (FastAPI + SQLModel)
├── requirements.txt      # Dépendances Python (versions pinées)
├── Dockerfile            # Image Docker pour exécuter l'app
├── docker-compose.yml    # Lancement simplifié avec Docker Compose
├── .dockerignore         # Fichiers ignorés par Docker
├── data/                 # (optionnel) dossier monté en volume pour SQLite
└── README.md             # Ce fichier
```