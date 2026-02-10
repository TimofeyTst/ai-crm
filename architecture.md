# Architecture Reference

**Stack:** Python 3.13, FastAPI, PostgreSQL, Docker

## Layered Architecture

```
1. Handlers     → entry points (API, background, cron, queue workers)
2. Services     → business logic, orchestration
3. Repositories → data access (DB, external services)
4. Connectors   → infrastructure (DB pools, storage, external clients)
```

**Data flow:** strictly top to bottom. Each layer depends only on the layer below.

## Handler Types

```
handlers/
├── api/            # HTTP endpoints (FastAPI routers)
├── background/     # Long-running background processes
├── cron/           # Scheduled periodic tasks
└── queue/          # Message queue consumers (RabbitMQ, etc.)
```

All handler types follow the same rule: **thin entry point → delegate to Service layer**.

A handler must never contain business logic. It parses input, calls a service, and formats the response.

## Package Structure

```
<project>/
├── api/                            # HTTP layer
│   ├── handlers/<domain>/          # Route handlers grouped by domain
│   ├── middlewares/                 # Auth, error handling, metrics
│   └── server.py                   # App factory, routing, lifecycle
│
├── internal/                       # Business logic layer
│   ├── services/<domain>/          # Service implementations
│   └── repositories/<storage>/     # Data access implementations
│       └── <domain>.py
│
├── pkg/                            # Shared infrastructure (reusable)
│   ├── configuration/              # Settings (pydantic-settings, env)
│   ├── connectors/                 # DB pools, storage, message brokers
│   ├── clients/                    # External API clients
│   ├── context/                    # Application context (DI container)
│   ├── utils/                      # Helpers (jwt, hashing, etc.)
│   └── models/                     # Shared models
│       ├── <domain>/               # Domain models (Pydantic)
│       ├── exceptions/             # Business exceptions per domain
│       ├── base/                   # Base classes (model, exception, enum)
│       ├── types/                  # Type definitions
│       └── consts/                 # Constants
│
├── background/                     # Background process entry points
├── cron/                           # Cron task entry points
├── queue/                          # Queue worker entry points
│
migrations/                         # DB migrations (SQL-based)
ci/                                 # Dockerfile, proxy configs
scripts/                            # Utility scripts
config/                             # Service configs
```

## Context Management

`WebContext` is the application-level DI container that holds shared resources (DB pools, clients, storage).

- Created once at app startup, stored in `app.state.web_context`
- Accessed in handlers via `Depends(web_context.get_web_context_dependency())`
- Passed explicitly through layers: Handler → Service → Repository
- Manages lifecycle: initializes resources on startup, cleans up on shutdown

```
Request → Handler(context) → Service(context) → Repository(context) → DB
```

Every service and repository function receives `context` as its first argument.

## Route Naming

All API routes follow: `/<version>/<entity>/<action>`

**Format:** `/v{N}/{entity}/{action}`

**Rules:**
- Version prefix: `v1`, `v2`, etc.
- Entity is plural: `users`, `resumes`, `sessions`
- Action is a verb: `create`, `list`, `upload`, `download`, `delete`, `update`
- Path parameters: `{id}` for resource identifiers

**Examples:**
```
/v1/auth/register
/v1/auth/login
/v1/users/list
/v1/resumes/upload
/v1/resumes/download/{id}
```

## Layer Rules

### Handlers (API / Background / Cron / Queue)

- Parse input, call service, return result
- No business logic
- Each handler type has its own entry point but shares the same services
- API handlers return HTTP responses; background/cron/queue handlers log results

### Services

- All business logic lives here
- Orchestrate multiple repositories and external clients
- Own transaction boundaries (transactor pattern)
- Never import other services directly — compose via DI if needed
- May call external clients for integrations

### Repositories

- Data access only (DB queries, file storage, cache)
- No business logic — pure CRUD + queries
- One repository per domain per storage type
- Return domain models, not raw DB rows

### Connectors & Clients

- Infrastructure wiring: connection pools, storage adapters, API clients
- Pluggable via factory pattern (e.g., local storage vs S3)
- Shared across all layers via application context

## Comments

Code should be self-explanatory through clear naming and structure.

- **Comment only non-obvious logic:** complex algorithms, business rules, workarounds, "why" decisions
- **Do not comment obvious code:** variable assignments, simple loops, standard CRUD
- **Prefer descriptive names over comments:** `calculate_user_monthly_revenue()` not `calc()` with a comment
- **No inline comments for self-evident code.** If code needs explanation, refactor first

## Patterns & Conventions

**Architecture:**
- Async everywhere (asyncpg, aiofiles, async handlers)
- Layered: Handler → Service → Repository → Storage
- WebContext as DI container, passed explicitly through layers
- Factory pattern for pluggable infrastructure (storage, clients)
- Pydantic models for validation and serialization

**Data access:**
- Direct SQL via asyncpg (no ORM)
- Connection pooling with per-task connection tracking
- Master/replica support with automatic host detection
- SQL migrations (sequential, versioned)

**Error handling:**
- Business errors: custom exception classes per domain inheriting base
- Technical errors: wrap with context using standard exceptions
- Errors propagate upward; handlers convert to appropriate response format

**Security:**
- JWT for user authentication (access + refresh tokens)
- Static token for internal/admin endpoints
- Password hashing via bcrypt
- Secrets via environment variables, never hardcoded

## Adding a New Domain

1. Define models in `pkg/models/<domain>/`
2. Define exceptions in `pkg/models/exceptions/<domain>.py`
3. Create repository in `internal/repositories/<storage>/<domain>.py`
4. Create service in `internal/services/<domain>/`
5. Create handler(s) in the appropriate handler type directory
6. Register routes/tasks in the entry point (server.py, cron config, etc.)
7. Add migration if new tables needed

## Development

```bash
# Dev (with infrastructure in Docker)
docker-compose -f docker-compose-dev.yaml up -d --build

# Prod
docker-compose -f docker-compose.yaml up -d --build
```

**Server:** gunicorn + uvicorn workers

**Linting:** ruff

**Dependencies:** Poetry

## Maintaining This Document

**Update when:**
- New layer or handler type is introduced
- New cross-cutting pattern is adopted
- Structural conventions change

**Keep it:**
- Generic — no endpoint lists, no DB schemas, no config values
- Concise — under 200 lines
- Prescriptive — describe how things should be, not how they are

**For AI agents:**
- Read this file at the start of every session
- Follow the layer rules strictly when adding new code
- All models are Pydantic, all I/O is async
- When in doubt about a pattern, ask before implementing
