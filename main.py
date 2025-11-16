from typing import List, Optional

from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()

class TodoBase(BaseModel):
    task: str = Field(..., min_length=1, max_length=200)
    done: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    task: Optional[str] = Field(None, min_length=1, max_length=200)
    done: Optional[bool] = None

class Todo(TodoBase):
    id: int

class TodoResponse(BaseModel):
    id: int
    task: str
    done: bool

class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)

class User(UserBase):
    id: int

class TodoCreatedResponse(BaseModel):
    message: str
    todo: Todo

class TodoUpdatedResponse(BaseModel):
    message: str
    todo: Todo

#base de donnees temporaire
medical_todos: List[Todo] = [
    Todo(id=1, task="prendre le medicament du matin"),
    Todo(id=2, task="faire un controle de la pression arterielle"),
]
users: List[User] = []

# les routes de l'API
#route racine
@app.get("/")
def read_root():
    print(" Route GET / appelée")
    return {"message": "API to-do medicale fonctionne!"}

#routes pour les taches medicales
@app.get(
    "/todos",
    response_model=List[TodoResponse],
    tags=["To-Do"],
    summary="Lister toutes les tâches",
    description="Retourne l'ensemble des tâches médicales enregistrées dans le système."
)
@app.get(
    "/todos/",
    response_model=List[TodoResponse],
    tags=["To-Do"],
    summary="Lister toutes les tâches",
    description="Retourne l'ensemble des tâches médicales enregistrées dans le système."
)
def get_todos():
    print(" Route GET /todos/ appelée")
    return medical_todos

#routes pour recuperer une tache par son id
@app.get(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    tags=["To-Do"],
    summary="Obtenir une tâche",
    description="Récupère une tâche spécifique par son identifiant."
)
def get_todo(todo_id: int):
    print(f" Route GET /todos/{todo_id} appelée")
    for todo in medical_todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tache non trouvee")

#route pour ajouter une nouvelle tache
@app.post(
    "/todos",
    response_model=TodoCreatedResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["To-Do"],
    summary="Créer une nouvelle tâche",
    description="Ajoute une nouvelle tâche médicale à la liste. Retourne la ressource créée."
)
@app.post(
    "/todos/",
    response_model=TodoCreatedResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["To-Do"],
    summary="Créer une nouvelle tâche",
    description="Ajoute une nouvelle tâche médicale à la liste. Retourne la ressource créée."
)
def add_todo(todo: TodoCreate):
    print(f"✅ Route POST /todos/ appelée - Nouvelle tâche: {todo.task}")
    new_id = (max((t.id for t in medical_todos), default=0) + 1)
    new_todo = Todo(id=new_id, **todo.model_dump())
    medical_todos.append(new_todo)
    return {"message": "Tâche ajoutée ✅", "todo": new_todo}

@app.put(
    "/todos/{todo_id}",
    response_model=TodoUpdatedResponse,
    tags=["To-Do"],
    summary="Mettre à jour une tâche",
    description="Remplace le contenu d'une tâche (titre et statut)."
)
def update_todo(todo_id: int, todo: TodoBase):
    for idx, existing in enumerate(medical_todos):
        if existing.id == todo_id:
            updated = Todo(id=existing.id, **todo.model_dump())
            medical_todos[idx] = updated
            return {"message": "Tâche mise à jour 🔄", "todo": updated}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tache non trouvee")

#route pour supprimer une tache
@app.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["To-Do"],
    summary="Supprimer une tâche",
    description="Supprime définitivement une tâche par identifiant. Retourne 204 en cas de succès."
)
def delete_todo(todo_id: int):
    for idx, existing in enumerate(medical_todos):
        if existing.id == todo_id:
            medical_todos.pop(idx)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tache non trouvee")

# Users endpoints minimalistes
@app.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED, tags=["users"])
def create_user(user: UserCreate):
    new_id = (max((u.id for u in users), default=0) + 1)
    created = User(id=new_id, name=user.name, email=user.email)
    users.append(created)
    return created

@app.get("/users/", response_model=List[User], tags=["users"])
def list_users():
    return users
