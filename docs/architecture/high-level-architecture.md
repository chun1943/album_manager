# High Level Architecture

## Technical Summary

Album Manager is a **single-file monolithic FastAPI application** with a simple, flat structure. The application follows a straightforward pattern:
- All API endpoints are defined in `main.py`
- Database models are in `models.py`
- Pydantic schemas are in `schemas.py`
- External service integration is in `musicbrainz_service.py`

**Architecture Pattern**: Simple monolithic REST API with no separation of concerns (controllers, services, repositories). All business logic is in route handlers.

## Actual Tech Stack

| Category          | Technology | Version | Notes                                    |
| ----------------- | ---------- | ------- | ---------------------------------------- |
| Runtime           | Python     | 3.x     | (version not specified in requirements)   |
| Framework         | FastAPI    | 0.115.12| ASGI web framework                       |
| ORM               | SQLAlchemy | 2.0.40  | Modern declarative style with Mapped     |
| Validation        | Pydantic   | 2.11.4  | Request/response validation               |
| Database          | SQLite     | -       | Default (can switch to PostgreSQL)      |
| Database Driver   | psycopg2   | 2.9.10  | For PostgreSQL (if used)                 |
| HTTP Client       | httpx      | 0.28.1  | Async HTTP client for external APIs      |
| ASGI Server       | Uvicorn    | 0.34.2  | Production ASGI server                   |
| Migration Tool    | Alembic    | 1.15.2  | **Available but NOT currently configured**|
| Config Management | python-dotenv | 1.1.0 | Environment variable loading             |
| Testing           | pytest     | 8.3.5   | **Available but NO tests exist**          |

## Repository Structure Reality Check

- **Type**: Simple monorepo (single application)
- **Package Manager**: pip (requirements.txt)
- **Notable**: 
  - Very flat structure - all code in root directory
  - No separation into src/, app/, or similar
  - No test directory exists
  - No Alembic migrations directory exists (despite Alembic being in requirements.txt)
  - Database file (`albums.db`) is in root directory
