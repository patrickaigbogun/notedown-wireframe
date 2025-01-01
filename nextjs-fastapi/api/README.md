# NoteDown API

FastAPI-powered backend service for secure note management with activity tracking.

## Prerequisites

- Python 3.10+
- PostgreSQL database
- Poetry package manager

## Dependencies

```toml
[tool.poetry.dependencies]
```

## Quick Start

1. Install Poetry:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install project dependencies:

```python
poetry install
```

3. configure database:
```env
DATABASE_URL = postgresql://user:password@localhost:5432/database
```

4. Run database migrations:
```bash
cd api/database
alembic revision --autogenerate -m "Initial setup"
alembic upgrade head
```

5. Run the application:
```python
poetry run uvicorn app:app --reload
```

### API Documentation
API documentation is available at
- Swagger UI: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

### Project Structure

```
api/
├── app.py              # FastAPI application
├── database/
│   ├── models.py       # SQLAlchemy models
│   ├── migrations/     # Alembic migrations
│   └── alembic.ini    # Migration config
└── README.md
```

