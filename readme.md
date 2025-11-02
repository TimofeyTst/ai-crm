## Fast setup
Create .env by .env.example copy

Create docker network
```
docker network create ai-crm-network
```

### Docker Compose (Production)

For production with external database:

```bash
cd ci
docker-compose -f docker-compose.yaml up -d
```

### Docker Compose (Development)

For local development with PostgreSQL:

```bash
cd ci
docker-compose -f docker-compose-dev.yaml up -d
```

## Development

### Install development dependencies

```bash
poetry install --with dev
```

### Linting and Formatting

The project uses `ruff` for linting and formatting.

**Check code quality:**
> --fix to fix
```bash
poetry run ruff check .
```

**Format code:**
```bash
poetry run ruff format .
```

**Run all checks (lint + format):**
```bash
poetry run ruff check --fix . && poetry run ruff format .
```

### Code Style Rules

- Maximum line length: **80 characters**
- Import sorting: automatic (isort via ruff)
- Unused imports: automatically removed
- Quote style: double quotes
- Indentation: 4 spaces

## Kubernetes TODO 

### Build Docker image for kubernetes 

```bash
# Build image
docker build -f ci/Dockerfile -t ai-crm:latest .

# Run container
docker run -p 8000:8000 ai-crm:latest
```