# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies for building native modules,
# including pkg-config and MySQL client development libraries.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    pkg-config \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install Python dependencies.
# Your requirements.txt includes:
# asgiref==3.8.1
# Django==5.1.7
# mysql-connector-python==9.2.0
# mysqlclient==2.2.7
# psycopg2-binary==2.9.10
# sqlparse==0.5.3
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the project source code into the container.
COPY . /app/

# Create the staticfiles directory (make sure STATIC_ROOT is defined in settings.py)
RUN mkdir -p /app/staticfiles

# Set the Django settings module environment variable.
ENV DJANGO_SETTINGS_MODULE=modular_project.settings

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port Cloud Run uses (8080)
EXPOSE 8080

# Use Gunicorn to serve the Django application.
CMD ["sh", "-c", "exec gunicorn modular_project.wsgi:application --bind 0.0.0.0:${PORT:-8080} --workers 3"]
