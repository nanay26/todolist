# Base image resmi Python versi ringan
FROM python:3.12-slim

# Working directory di dalam container
WORKDIR /app

# Salin daftar dependency lebih dulu (memanfaatkan Docker layer cache)
COPY requirements.txt .

# Instalasi dependency
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh source code aplikasi
COPY app/ ./app/
COPY tests/ ./tests/

# Port yang digunakan aplikasi (FastAPI/Uvicorn)
EXPOSE 8000

# Perintah untuk menjalankan aplikasi
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
