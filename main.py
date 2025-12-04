from typing import Optional, List
import logging
import os

from fastapi import FastAPI, HTTPException, Response, status
from sqlmodel import Field, SQLModel, Session, create_engine, select

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./medbridge.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task: str
    done: bool = False


class TodoCreate(SQLModel):
    task: str


class TodoRead(SQLModel):
    id: int
    task: str
    done: bool


class TodoUpdate(SQLModel):
    task: Optional[str] = None
    done: Optional[bool] = None


app = FastAPI(title="MedBridge To-Do API")


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    logger.info("Database tables created/verified")
    # seed initial data if table is empty
    with Session(engine) as session:
        count = session.exec(select(Todo)).count()
        if count == 0:
            logger.info("Seeding initial todos into database")
            sample = [
                Todo(task="prendre le medicament du matin"),
                Todo(task="faire un controle de la pression arterielle"),
            ]
            session.add_all(sample)
            session.commit()


@app.get(
    "/",
    summary="Point d'entree de l'API",
    description="Retourne un message indiquant que l'API to-do medicale fonctionne correctement.",
)
def read_root():
    logger.info("Route GET / appelée")
    return {"message": "API to-do medicale fonctionne!"}


@app.get(
    "/todos/",
    tags=["To-Do"],
    summary="Lister toutes les taches medicales",
    description="Retourne l'ensemble des taches medicales enregistrees dans le systeme.",
    response_model=List[TodoRead],
)
def get_todos():
    logger.info("Route GET /todos/ appelée")
    with Session(engine) as session:
        todos = session.exec(select(Todo)).all()
        return todos


@app.get(
    "/todos/{todo_id}",
    tags=["To-Do"],
    response_model=TodoRead,
    summary="Obtenir une tache precise",
    description="Recupere une tache medicale a partir de son identifiant unique.",
)
def get_todo(todo_id: int):
    logger.info("Route GET /todos/%s appelée", todo_id)
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Tache non trouvee")
        return todo


@app.post(
    "/todos/",
    tags=["To-Do"],
    summary="Creer une nouvelle tache",
    description="Ajoute une entree dans la liste To-Do medicale.",
    status_code=status.HTTP_201_CREATED,
    response_model=TodoRead,
)
def add_todo(todo: TodoCreate, response: Response):
    logger.info("Route POST /todos/ appelée - Nouvelle tâche: %s", todo.task)
    new_todo = Todo(task=todo.task)
    with Session(engine) as session:
        session.add(new_todo)
        session.commit()
        session.refresh(new_todo)
        response.headers["Location"] = f"/todos/{new_todo.id}"
        return new_todo


@app.patch(
    "/todos/{todo_id}",
    tags=["To-Do"],
    summary="Mettre a jour partiellement une tache",
    response_model=TodoRead,
)
def patch_todo(todo_id: int, todo_update: TodoUpdate):
    logger.info("Route PATCH /todos/%s appelée", todo_id)
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Tache non trouvee")
        if todo_update.task is not None:
            todo.task = todo_update.task
        if todo_update.done is not None:
            todo.done = todo_update.done
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo


@app.delete(
    "/todos/{todo_id}",
    tags=["To-Do"],
    summary="Supprimer une tache",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_todo(todo_id: int):
    logger.info("Route DELETE /todos/%s appelée", todo_id)
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Tache non trouvee")
        session.delete(todo)
        session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
