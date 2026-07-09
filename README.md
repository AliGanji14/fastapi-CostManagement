# Cost Management API

## Short Description

Cost Management API is a FastAPI-based backend for tracking personal expenses. It provides user authentication, expense CRUD operations, PostgreSQL persistence, Redis-backed caching, internationalization support, and Sentry error monitoring.

## Features

- User registration, login, logout, and JWT cookie-based session refresh
- Create, read, update, delete, and search expenses
- Per-user expense access control
- PostgreSQL database with SQLAlchemy and Alembic migrations
- Redis caching for external weather data
- Interactive API documentation with Swagger UI
- Docker-based local development environment
- Basic i18n support for English and Persian messages

## Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis
- Alembic
- Docker and Docker Compose
- Pytest
- Locust
- Sentry

## Installation

```bash
git clone https://github.com/AliGanji14/fastapi-CostManagement.git
cd fastapi-CostManagement
```

Create `core/.env` with the required settings:

```env
SQLALCHEMY_DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres
JWT_SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_SECONDS=900
REFRESH_TOKEN_EXPIRE_SECONDS=604800
COOKIE_SECURE=false
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
REDIS_URL=redis://redis:6379
SENTRY_DSN=
```

Start the services:

```bash
docker compose up --build
```

## Usage

Open the API documentation:

```text
http://localhost:8000/docs
```

Health check:

```bash
curl http://localhost:8000/is_ready
```

Run tests locally from the `core` directory after installing dependencies:

```bash
pytest
```

## Project Structure (brief)

```text
core/
├── auth/          # JWT and authentication helpers
├── core/          # Configuration, database, i18n, exceptions
├── expenses/      # Expense models, schemas, and routes
├── users/         # User models, schemas, and routes
├── migrations/    # Alembic migration files
├── tests/         # Pytest test suite
└── main.py        # FastAPI application entry point
```

## API Endpoints (if applicable)

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/users/register` | Register a user |
| POST | `/users/login` | Log in and set auth cookies |
| POST | `/users/refresh-token` | Refresh the session |
| POST | `/users/logout` | Log out and clear auth cookies |
| GET | `/expenses` | List or search expenses |
| POST | `/expenses` | Create an expense |
| GET | `/expenses/{expense_id}` | Get one expense |
| PUT | `/expenses/{expense_id}` | Update an expense |
| DELETE | `/expenses/{expense_id}` | Delete an expense |
| GET | `/fetch-current-weather` | Fetch cached current weather data |
| GET | `/is_ready` | Readiness check |

## Author

Ali Ganji — [GitHub](https://github.com/AliGanji14)
