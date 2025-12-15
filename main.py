from typing import List, Optional

import logging
from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from medbridge import db, models, schemas, security

app = FastAPI(title="API Médicale To-Do", version="1.0.0")

logger = logging.getLogger(__name__)


@app.get("/")
def read_root():
    logger.debug("GET /")
    return {"message": "API to-do medicale fonctionne!"}

# Routes pour les tâches médicales - SUPPRIMER LES DOUBLONS
@app.get(
    "/todos",
    response_model=List[schemas.TodoRead],
    tags=["To-Do"],
    summary="Lister toutes les tâches",
    description="Retourne l'ensemble des tâches médicales enregistrées dans le système."
)
async def get_todos(session: AsyncSession = Depends(db.get_session)):
    logger.debug("GET /todos")
    result = await session.execute(select(models.Todo))
    todos = result.scalars().all()
    return todos

@app.get(
    "/todos/{todo_id}",
    response_model=schemas.TodoRead,
    tags=["To-Do"],
    summary="Obtenir une tâche",
    description="Récupère une tâche spécifique par son identifiant."
)
async def get_todo(todo_id: int, session: AsyncSession = Depends(db.get_session)):
    logger.debug("GET /todos/%s", todo_id)
    result = await session.execute(select(models.Todo).filter_by(id=todo_id))
    todo = result.scalar_one_or_none()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tâche non trouvée")
    return todo

@app.post(
    "/todos",
    response_model=schemas.TodoRead,
    status_code=status.HTTP_201_CREATED,
    tags=["To-Do"],
    summary="Créer une nouvelle tâche",
    description="Ajoute une nouvelle tâche médicale à la liste. Retourne la ressource créée."
)
async def add_todo(todo: schemas.TodoCreate, session: AsyncSession = Depends(db.get_session)):
    logger.info("POST /todos: %s", todo.task)
    # If owner_id provided, ensure the user exists
    if todo.owner_id is not None:
        user = await session.get(models.User, todo.owner_id)
        if user is None:
            raise HTTPException(status_code=400, detail="Owner user not found")

    db_todo = models.Todo(task=todo.task, done=todo.done, owner_id=todo.owner_id)
    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)
    return db_todo

@app.put(
    "/todos/{todo_id}",
    response_model=schemas.TodoRead,
    tags=["To-Do"],
    summary="Mettre à jour une tâche",
    description="Remplace le contenu d'une tâche (titre et statut)."
)
async def update_todo(todo_id: int, todo: schemas.TodoBase, session: AsyncSession = Depends(db.get_session)):
    result = await session.execute(select(models.Todo).filter_by(id=todo_id))
    db_todo = result.scalar_one_or_none()
    if db_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tâche non trouvée")
    db_todo.task = todo.task
    db_todo.done = todo.done
    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)
    return db_todo

# Endpoint PATCH pour mise à jour partielle
@app.patch(
    "/todos/{todo_id}",
    response_model=schemas.TodoRead,
    tags=["To-Do"],
    summary="Mettre à jour partiellement une tâche",
    description="Met à jour partiellement une tâche (un ou plusieurs champs)."
)
async def partial_update_todo(todo_id: int, todo_update: schemas.TodoBase | dict, session: AsyncSession = Depends(db.get_session)):
    result = await session.execute(select(models.Todo).filter_by(id=todo_id))
    db_todo = result.scalar_one_or_none()
    if db_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tâche non trouvée")

    # Apply partial updates
    update_data = todo_update if isinstance(todo_update, dict) else todo_update.model_dump(exclude_unset=True)
    if "task" in update_data:
        db_todo.task = update_data["task"]
    if "done" in update_data:
        db_todo.done = update_data["done"]

    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)
    return db_todo

@app.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["To-Do"],
    summary="Supprimer une tâche",
    description="Supprime définitivement une tâche par identifiant. Retourne 204 en cas de succès."
)
async def delete_todo(todo_id: int, session: AsyncSession = Depends(db.get_session)):
    result = await session.execute(select(models.Todo).filter_by(id=todo_id))
    db_todo = result.scalar_one_or_none()
    if db_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tâche non trouvée")
    await session.delete(db_todo)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Users endpoints
@app.post("/users/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED, tags=["Users"])
async def create_user(user: schemas.UserCreate, session: AsyncSession = Depends(db.get_session)):
    # Prevent duplicate email
    result = await session.execute(select(models.User).filter_by(email=user.email))
    existing = result.scalar_one_or_none()
    if existing is not None:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = security.hash_password(user.password)
    db_user = models.User(name=user.name, email=user.email, hashed_password=hashed)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


@app.get("/users/", response_model=List[schemas.UserRead], tags=["Users"])
async def list_users(session: AsyncSession = Depends(db.get_session)):
    result = await session.execute(select(models.User))
    users = result.scalars().all()
    return users

# Statistiques (bonus)
@app.get("/stats", tags=["Statistiques"])
async def get_stats(session: AsyncSession = Depends(db.get_session)):
    total_todos = await session.scalar(select(func.count()).select_from(models.Todo))
    completed_todos = await session.scalar(select(func.count()).select_from(models.Todo).filter_by(done=True))
    total_users = await session.scalar(select(func.count()).select_from(models.User))
    pending = (total_todos or 0) - (completed_todos or 0)
    return {
        "total_todos": total_todos or 0,
        "completed_todos": completed_todos or 0,
        "pending_todos": pending or 0,
        "total_users": total_users or 0,
    }


@app.on_event("startup")
async def on_startup():
    logger.info("Initialising database (creating tables if needed)")
    await db.init_db()