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

## Kubernetes TODO 

### Build Docker image for kubernetes 

```bash
# Build image
docker build -f ci/Dockerfile -t ai-crm:latest .

# Run container
docker run -p 8000:8000 ai-crm:latest
```