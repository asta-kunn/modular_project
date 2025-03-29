# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Disable .pyc generation and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies (adjust if necessary for your project)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the project code
COPY . /app/

# Ensure STATIC_ROOT directory exists (as defined in your settings.py)
RUN mkdir -p /app/staticfiles

# Set the Django settings module (if needed)
ENV DJANGO_SETTINGS_MODULE=modular_project.settings

# Run collectstatic to gather all static files
RUN python manage.py collectstatic --noinput

# Expose port 8080 (Cloud Run default)
EXPOSE 8080

# Use Gunicorn to serve the application
CMD ["gunicorn", "modular_project.wsgi:application", "--bind", "0.0.0.0:8080", "--workers", "3"]
