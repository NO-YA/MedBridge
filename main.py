from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "de bienvenue! sur mon application medicale"}
