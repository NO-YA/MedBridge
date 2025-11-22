from typing import List, Optional
from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel, Field, EmailStr

app = FastAPI(title="API Médicale To-Do", version="1.0.0")

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

# Base de données temporaire
medical_todos: List[Todo] = [
    Todo(id=1, task="prendre le medicament du matin", done=False),
    Todo(id=2, task="faire un controle de la pression arterielle", done=False),
]
users: List[User] = []

# Fonction utilitaire pour trouver une tâche
def find_todo_by_id(todo_id: int) -> Optional[Todo]:
    return next((todo for todo in medical_todos if todo.id == todo_id), None)

def find_todo_index_by_id(todo_id: int) -> Optional[int]:
    return next((idx for idx, todo in enumerate(medical_todos) if todo.id == todo_id), None)

# Les routes de l'API
@app.get("/")
def read_root():
    print(" Route GET / appelée")
    return {"message": "API to-do medicale fonctionne!"}

# Routes pour les tâches médicales - SUPPRIMER LES DOUBLONS
@app.get(
    "/todos",
    response_model=List[TodoResponse],
    tags=["To-Do"],
    summary="Lister toutes les tâches",
    description="Retourne l'ensemble des tâches médicales enregistrées dans le système."
)
def get_todos():
    print(" Route GET /todos appelée")
    return medical_todos

@app.get(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    tags=["To-Do"],
    summary="Obtenir une tâche",
    description="Récupère une tâche spécifique par son identifiant."
)
def get_todo(todo_id: int):
    print(f" Route GET /todos/{todo_id} appelée")
    todo = find_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Tâche non trouvée"
        )
    return todo

@app.post(
    "/todos",
    response_model=TodoCreatedResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["To-Do"],
    summary="Créer une nouvelle tâche",
    description="Ajoute une nouvelle tâche médicale à la liste. Retourne la ressource créée."
)
def add_todo(todo: TodoCreate):
    print(f" Route POST /todos appelée - Nouvelle tâche: {todo.task}")
    new_id = max((t.id for t in medical_todos), default=0) + 1
    new_todo = Todo(id=new_id, **todo.model_dump())
    medical_todos.append(new_todo)
    return {"message": "Tâche ajoutée ", "todo": new_todo}

@app.put(
    "/todos/{todo_id}",
    response_model=TodoUpdatedResponse,
    tags=["To-Do"],
    summary="Mettre à jour une tâche",
    description="Remplace le contenu d'une tâche (titre et statut)."
)
def update_todo(todo_id: int, todo: TodoBase):
    todo_index = find_todo_index_by_id(todo_id)
    if todo_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Tâche non trouvée"
        )
    
    updated_todo = Todo(id=todo_id, **todo.model_dump())
    medical_todos[todo_index] = updated_todo
    return {"message": "Tâche mise à jour 🔄", "todo": updated_todo}

# Endpoint PATCH pour mise à jour partielle
@app.patch(
    "/todos/{todo_id}",
    response_model=TodoUpdatedResponse,
    tags=["To-Do"],
    summary="Mettre à jour partiellement une tâche",
    description="Met à jour partiellement une tâche (un ou plusieurs champs)."
)
def partial_update_todo(todo_id: int, todo_update: TodoUpdate):
    todo_index = find_todo_index_by_id(todo_id)
    if todo_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Tâche non trouvée"
        )
    
    existing_todo = medical_todos[todo_index]
    update_data = todo_update.model_dump(exclude_unset=True)
    updated_todo = Todo(
        id=todo_id,
        task=update_data.get('task', existing_todo.task),
        done=update_data.get('done', existing_todo.done)
    )
    medical_todos[todo_index] = updated_todo
    return {"message": "Tâche partiellement mise à jour 🔄", "todo": updated_todo}

@app.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["To-Do"],
    summary="Supprimer une tâche",
    description="Supprime définitivement une tâche par identifiant. Retourne 204 en cas de succès."
)
def delete_todo(todo_id: int):
    todo_index = find_todo_index_by_id(todo_id)
    if todo_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Tâche non trouvée"
        )
    
    medical_todos.pop(todo_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Users endpoints
@app.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_user(user: UserCreate):
    new_id = max((u.id for u in users), default=0) + 1
    created = User(id=new_id, name=user.name, email=user.email)
    users.append(created)
    return created

@app.get("/users/", response_model=List[User], tags=["Users"])
def list_users():
    return users

# Statistiques (bonus)
@app.get("/stats", tags=["Statistiques"])
def get_stats():
    total_todos = len(medical_todos)
    completed_todos = sum(1 for todo in medical_todos if todo.done)
    pending_todos = total_todos - completed_todos
    
    return {
        "total_todos": total_todos,
        "completed_todos": completed_todos,
        "pending_todos": pending_todos,
        "total_users": len(users)
    }