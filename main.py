from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Todo(BaseModel):
    task: str

#base de donnees temporaire
medical_todos = [
    {"id": 1, "task": "prendre le medicament du matin"},
    {"id": 2, "task": "faire un controle de la pression arterielle"},
]

# les routes de l'API
#route racine
@app.get("/")
def read_root():
    print(" Route GET / appelée")
    return {"message": "API to-do medicale fonctionne!"}

#routes pour les taches medicales
@app.get("/todos/")
def get_todos():
    print(" Route GET /todos/ appelée")
    return {"todos": medical_todos}

#routes pour recuperer une tache par son id
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    print(f" Route GET /todos/{todo_id} appelée")
    for todo in medical_todos:
        if todo["id"] == todo_id:
            return todo
    return {"error": "Tache non trouvee"}

#route pour ajouter une nouvelle tache
@app.post("/todos/")
def add_todo(todo: Todo):
    print(f"✅ Route POST /todos/ appelée - Nouvelle tâche: {todo.task}")
    new_id = len(medical_todos) + 1
    new_todo = {"id": new_id, "task": todo.task}
    medical_todos.append(new_todo)
    return {"message": "Tache ajoutee avec succes", "todo": new_todo}
