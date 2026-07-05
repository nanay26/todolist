"""
Todo List API - Aplikasi sederhana untuk Tugas Praktikum Terintegrasi
Docker, Container Orchestration, dan CI/CD.

Menyediakan:
- GET  /              -> info aplikasi
- GET  /health        -> health check (dipakai untuk pengujian & bukti "aplikasi dapat diakses")
- GET  /todos         -> daftar semua todo
- POST /todos         -> tambah todo baru
- GET  /todos/{id}    -> ambil satu todo
- PUT  /todos/{id}    -> update status selesai/belum
- DELETE /todos/{id}  -> hapus todo
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Todo List API", version="1.0.0")

# Penyimpanan sederhana in-memory (cukup untuk keperluan demo praktikum)
todos_db = {}
next_id = 1


class TodoCreate(BaseModel):
    title: str
    done: bool = False


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


class Todo(TodoCreate):
    id: int


@app.get("/")
def root():
    return {
        "app": "Todo List API",
        "version": "1.0.0",
        "message": "Selamat datang di Todo List API",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(todo: TodoCreate):
    global next_id
    new_todo = Todo(id=next_id, title=todo.title, done=todo.done)
    todos_db[next_id] = new_todo
    next_id += 1
    return new_todo


@app.get("/todos")
def list_todos():
    return list(todos_db.values())


@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    todo = todos_db.get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo tidak ditemukan")
    return todo


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, update: TodoUpdate):
    todo = todos_db.get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo tidak ditemukan")
    if update.title is not None:
        todo.title = update.title
    if update.done is not None:
        todo.done = update.done
    todos_db[todo_id] = todo
    return todo


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo tidak ditemukan")
    del todos_db[todo_id]
    return None
