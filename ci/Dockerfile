FROM python:3.13-slim

# Configure system
RUN apt-get update && \
    apt-get install -y gcc libpq-dev curl build-essential && \
    apt clean && \
    rm -rf /var/cache/apt/* && \
    rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=2.2.1
RUN pip install -U pip && \
    pip install poetry==${POETRY_VERSION}

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=false \
    POETRY_CACHE_DIR=/tmp/poetry_cache

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8

# Build & install dependencies
WORKDIR /app
COPY . .

RUN poetry install
RUN rm -rf $POETRY_CACHE_DIR

# Finish, configure scripts
ENV PATH "$PATH:/ai-crm/scripts"

RUN useradd -m -d /app -s /bin/bash app \
    && chown -R app:app /app/* && chmod +x /app/scripts/*

USER app
