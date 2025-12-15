import os
import asyncio

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def set_env_for_tests(monkeypatch):
    # Use in-memory SQLite for tests
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")


@pytest.fixture()
def client():
    # Import after env var set
    import importlib

    importlib.reload(importlib.import_module("medbridge.db"))
    from medbridge import db

    # Create tables for the in-memory DB
    asyncio.run(db.init_db())

    # Now import app (which will use medbridge.db)
    import main as app_module

    client = TestClient(app_module.app)
    yield client


def test_create_user_and_todo(client: TestClient):
    # Create a user
    r = client.post("/users/", json={"name": "Alice", "email": "alice@example.com", "password": "supersecret"})
    assert r.status_code == 201
    user = r.json()
    assert user["email"] == "alice@example.com"

    # Create a todo with owner
    r2 = client.post("/todos", json={"task": "Prendre medicament", "done": False, "owner_id": user["id"]})
    assert r2.status_code == 201
    todo = r2.json()
    assert todo["task"] == "Prendre medicament"

    # Fetch todos
    r3 = client.get("/todos")
    assert r3.status_code == 200
    assert len(r3.json()) >= 1


def test_create_user_long_password(client: TestClient):
    long_pwd = "x" * 200
    r = client.post("/users/", json={"name": "Bob", "email": "bob@example.com", "password": long_pwd})
    assert r.status_code == 201
    user = r.json()
    assert user["email"] == "bob@example.com"
