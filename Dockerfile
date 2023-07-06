# Base image with Python and PostgreSQL client
FROM python:3.9-slim-buster as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        gcc \
        python3-dev \
        musl-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /onlinecourse

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

FROM base AS development
ENV DJANGO_SETTINGS_MODULE=online_courses.settings.development
CMD python manage.py runserver 0.0.0.0:80000

FROM base AS production
ENV DJANGO_SETTINGS_MODULE=online_courses.settings.production
CMD python manage.py runserver 0.0.0.0:8000