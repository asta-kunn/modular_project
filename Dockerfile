# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Jangan tulis file bytecode dan pastikan output log langsung tampil di konsol
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependensi sistem (misalnya build-essential dan libpq-dev untuk PostgreSQL, jika diperlukan)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy file requirements.txt dan install dependensi Python
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Salin seluruh kode proyek ke dalam container
COPY . /app/

# Kumpulkan static files (pastikan setting STATIC_ROOT sudah diatur di settings.py)
RUN python manage.py collectstatic --noinput

# Expose port 8080 (Cloud Run menggunakan port 8080 secara default)
EXPOSE 8080

# Jalankan aplikasi menggunakan Gunicorn dengan 3 worker
CMD ["gunicorn", "modular_project.wsgi:application", "--bind", "0.0.0.0:8080", "--workers", "3"]
