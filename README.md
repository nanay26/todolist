# Todo List API

Aplikasi REST API sederhana untuk mengelola daftar todo, dibangun dengan **FastAPI (Python)**.
Proyek ini dibuat untuk **Tugas Praktikum Terintegrasi: Docker, Container Orchestration, dan CI/CD** — Mata Kuliah Komputasi Awan.

## Struktur Proyek

```
todo-api/
├── app/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_main.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── .github/
    └── workflows/
        └── ci.yml
```

## Endpoint

| Method | Path          | Keterangan                     |
|--------|---------------|---------------------------------|
| GET    | `/`           | Info aplikasi                  |
| GET    | `/health`     | Health check (`{"status":"healthy"}`) |
| GET    | `/todos`      | Daftar semua todo               |
| POST   | `/todos`      | Tambah todo baru                |
| GET    | `/todos/{id}` | Ambil satu todo                 |
| PUT    | `/todos/{id}` | Update todo                     |
| DELETE | `/todos/{id}` | Hapus todo                      |

## Menjalankan Secara Lokal (tanpa Docker)

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Buka `http://localhost:8000/docs` untuk dokumentasi interaktif (Swagger UI).

## Menjalankan Automated Test

```bash
pytest -v
```

## Menjalankan dengan Docker

```bash
docker build -t todo-api:v1 .
docker run -d --name todo-api -p 8080:8000 todo-api:v1
```

Akses di `http://localhost:8080/health`.

## Menjalankan dengan Docker Compose

```bash
docker compose up -d
docker compose ps
docker compose down
```

## CI/CD

Pipeline GitHub Actions (`.github/workflows/ci.yml`) otomatis menjalankan:
1. Checkout source code
2. Setup Python
3. Install dependency
4. Menjalankan automated test (`pytest`)
5. Build Docker image

Pipeline berjalan setiap kali ada `push` atau `pull request` ke branch `main`.
