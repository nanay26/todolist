"""
Automated test untuk Todo List API.
Menjalankan pengujian: root endpoint, health check, dan alur CRUD todo.

Jalankan secara lokal dengan:
    pytest -v
"""

from fastapi.testclient import TestClient
from app.main import app, todos_db

client = TestClient(app)


def setup_function():
    """Reset penyimpanan sebelum setiap test agar tidak saling bergantung."""
    todos_db.clear()


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["app"] == "Todo List API"


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_todo():
    response = client.post("/todos", json={"title": "Belajar Docker"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Belajar Docker"
    assert data["done"] is False
    assert data["id"] == 1


def test_list_todos():
    client.post("/todos", json={"title": "Belajar Docker"})
    client.post("/todos", json={"title": "Belajar CI/CD"})
    response = client.get("/todos")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_todo_not_found():
    response = client.get("/todos/999")
    assert response.status_code == 404


def test_update_todo():
    create_res = client.post("/todos", json={"title": "Belajar Compose"})
    todo_id = create_res.json()["id"]
    update_res = client.put(f"/todos/{todo_id}", json={"done": True})
    assert update_res.status_code == 200
    assert update_res.json()["done"] is True


def test_delete_todo():
    create_res = client.post("/todos", json={"title": "Hapus saya"})
    todo_id = create_res.json()["id"]
    delete_res = client.delete(f"/todos/{todo_id}")
    assert delete_res.status_code == 204
    get_res = client.get(f"/todos/{todo_id}")
    assert get_res.status_code == 404
