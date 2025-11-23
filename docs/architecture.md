# Album Manager Brownfield Architecture Document

## Introduction

This document captures the CURRENT STATE of the Album Manager codebase, including technical debt, workarounds, and real-world patterns. It serves as a reference for AI agents working on enhancements.

### Document Scope

**Focused on areas relevant to: 專輯自動辨識與進階管理功能增強**

This documentation focuses on the modules and areas that will be affected by the planned enhancement:
- Data models (Album, User)
- API endpoints (album management, search)
- MusicBrainz integration service
- Database schema and migrations
- Search and filtering functionality

### Change Log

| Date       | Version | Description                 | Author      |
| ---------- | ------- | --------------------------- | ----------- |
| 2025-11-23 | 1.0     | Initial brownfield analysis | Architect   |

## Quick Reference - Key Files and Entry Points

### Critical Files for Understanding the System

- **Main Entry**: `main.py` - FastAPI application entry point
- **Configuration**: `database.py` - Database connection and session management
- **Core Business Logic**: `main.py` - All API endpoints and business logic
- **Data Models**: `models.py` - SQLAlchemy ORM models (User, Album)
- **API Schemas**: `schemas.py` - Pydantic request/response models
- **External Service**: `musicbrainz_service.py` - MusicBrainz API integration
- **Utilities**: `utils.py` - Title normalization helper

### Enhancement Impact Areas

Based on the PRD, these files will be affected:

**Must Modify:**
- `models.py` - Add new fields (year, genre, cover_url) to Album model
- `schemas.py` - Update AlbumCreate, AlbumUpdate, AlbumOut to include new fields
- `musicbrainz_service.py` - Enhance to extract year, genre, cover_url from API responses
- `main.py` - Add new endpoints (scan, recognize) and enhance search functionality

**May Need Modification:**
- `database.py` - May need Alembic migration setup (currently using Base.metadata.create_all)
- New file: Alembic migration scripts for schema changes
- New file: Image recognition service (for Story 1.5)

## High Level Architecture

### Technical Summary

Album Manager is a **single-file monolithic FastAPI application** with a simple, flat structure. The application follows a straightforward pattern:
- All API endpoints are defined in `main.py`
- Database models are in `models.py`
- Pydantic schemas are in `schemas.py`
- External service integration is in `musicbrainz_service.py`

**Architecture Pattern**: Simple monolithic REST API with no separation of concerns (controllers, services, repositories). All business logic is in route handlers.

### Actual Tech Stack

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

### Repository Structure Reality Check

- **Type**: Simple monorepo (single application)
- **Package Manager**: pip (requirements.txt)
- **Notable**: 
  - Very flat structure - all code in root directory
  - No separation into src/, app/, or similar
  - No test directory exists
  - No Alembic migrations directory exists (despite Alembic being in requirements.txt)
  - Database file (`albums.db`) is in root directory

## Source Tree and Module Organization

### Project Structure (Actual)

```text
album_manager/
├── main.py                    # FastAPI app + all API endpoints
├── models.py                  # SQLAlchemy ORM models
├── schemas.py                 # Pydantic request/response models
├── database.py                # Database connection and session factory
├── musicbrainz_service.py    # MusicBrainz API integration
├── utils.py                   # Utility functions (normalize_title)
├── view_db.py                 # Utility script to view database contents
├── requirements.txt           # Python dependencies
├── albums.db                  # SQLite database file (in root - not ideal)
├── docs/                      # Documentation (recently added)
│   ├── prd.md
│   └── prd/                   # Sharded PRD files
└── web-bundles/               # BMad agent definitions (not part of app)
```

### Key Modules and Their Purpose

- **Main Application** (`main.py`): 
  - Contains ALL API endpoints (user management, album CRUD, search)
  - All business logic is in route handlers (no service layer)
  - Uses FastAPI dependency injection for database sessions
  - CORS middleware configured for all origins (development mode)

- **Data Models** (`models.py`):
  - `User`: Simple user model with username (no authentication/authorization)
  - `Album`: Album model with title, normalized_title, barcode, artist, owner_id
  - Uses SQLAlchemy 2.0 style with `Mapped` type hints
  - Has unique constraints and indexes for data integrity

- **API Schemas** (`schemas.py`):
  - Pydantic models for request/response validation
  - `UserCreate`, `UserOut` for user operations
  - `AlbumCreate`, `AlbumUpdate`, `AlbumOut` for album operations
  - `ExistsOut` for album existence checks

- **Database** (`database.py`):
  - Simple database connection setup
  - Uses environment variable `DATABASE_URL` (defaults to SQLite)
  - Session factory with proper cleanup
  - **CRITICAL**: Currently uses `Base.metadata.create_all()` for schema creation (not migrations)

- **MusicBrainz Service** (`musicbrainz_service.py`):
  - Async HTTP client for MusicBrainz API
  - `search_by_barcode()` method returns structured dict
  - **NOTE**: Already extracts year, genre, cover_url but these are NOT stored in database
  - Uses singleton pattern (`musicbrainz_service` instance)

- **Utilities** (`utils.py`):
  - `normalize_title()`: Normalizes album titles for case-insensitive search
  - Simple string manipulation (strip, lower, collapse whitespace)

## Data Models and APIs

### Data Models

**User Model** (`models.py`):
- `id`: Primary key (Integer)
- `username`: Unique string (100 chars max)
- Relationship: `albums` (one-to-many with Album)

**Album Model** (`models.py`):
- `id`: Primary key (Integer)
- `title`: String (255 chars, indexed)
- `normalized_title`: String (255 chars, indexed) - for case-insensitive search
- `barcode`: Optional String (64 chars, nullable, indexed)
- `artist`: Optional String (255 chars, nullable)
- `owner_id`: Foreign key to User (CASCADE delete)
- **Constraints**:
  - Unique constraint on (`owner_id`, `normalized_title`)
  - Unique constraint on (`owner_id`, `barcode`)
  - Indexes on (`owner_id`, `normalized_title`) and (`owner_id`, `barcode`)

**Missing Fields** (to be added per PRD):
- `year`: Integer (nullable)
- `genre`: String(100) (nullable)
- `cover_url`: String(500) (nullable)

### API Specifications

**Current API Endpoints** (`main.py`):

**User Endpoints:**
- `POST /users` - Create user (returns existing if username exists)
- `GET /users/{user_id}` - Get user by ID

**Album Endpoints:**
- `POST /users/{user_id}/albums` - Create album (with duplicate checking)
- `GET /users/{user_id}/albums` - List albums (with optional title search via `q` parameter)
- `GET /users/{user_id}/albums/check` - Check if album exists (by title or barcode)
- `PUT /users/{user_id}/albums/{album_id}` - Update album
- `DELETE /users/{user_id}/albums/{album_id}` - Delete album

**External API:**
- `GET /api/search/barcode/{barcode}` - Search MusicBrainz by barcode (returns dict, not Album model)

**Utility:**
- `GET /healthz` - Health check

**API Response Format:**
- Uses Pydantic models for automatic validation and serialization
- FastAPI automatically generates OpenAPI/Swagger docs at `/docs`

**Error Handling:**
- Uses HTTPException with custom status codes:
  - 401: Creation/update failures
  - 405: Not found
  - 410: Duplicate (already exists)
  - 423: Validation error (missing required fields)

## Technical Debt and Known Issues

### Critical Technical Debt

1. **No Database Migrations**: 
   - Uses `Base.metadata.create_all()` instead of Alembic migrations
   - **Impact**: Cannot safely modify schema in production
   - **Action Required**: Set up Alembic for Story 1.1

2. **No Test Suite**:
   - pytest is in requirements.txt but no tests exist
   - **Impact**: No automated verification of functionality
   - **Risk**: Changes may break existing functionality

3. **Monolithic Main File**:
   - All business logic in `main.py` route handlers
   - **Impact**: Hard to test, maintain, and extend
   - **Note**: Acceptable for current scale, but will become problematic

4. **Database File in Root**:
   - `albums.db` in project root
   - **Impact**: May be accidentally committed or deleted
   - **Better**: Move to `data/` or `.data/` directory

5. **No Error Logging**:
   - Errors are printed to console or returned as HTTP responses
   - **Impact**: No audit trail or debugging capability
   - **Missing**: Proper logging setup

6. **CORS Wide Open**:
   - `allow_origins=["*"]` in development
   - **Impact**: Security risk in production
   - **Action**: Configure proper CORS for production

7. **Typo in Code**:
   - Line 179 in `main.py`: `user_idi` instead of `user_id` (typo)
   - **Impact**: Will cause runtime error
   - **Action**: Fix immediately

### Workarounds and Gotchas

- **Duplicate User Creation**: If username exists, returns existing user instead of error (line 36-37 in main.py)
- **Title Normalization**: Must use `normalize_title()` consistently for search to work
- **Barcode Search**: MusicBrainz service already returns year/genre/cover_url but they're not stored
- **Session Management**: Uses `autoflush=False, autocommit=False` - must explicitly commit
- **SQLite Thread Safety**: `check_same_thread=False` is set for SQLite (required for FastAPI)

## Integration Points and External Dependencies

### External Services

| Service      | Purpose              | Integration Type | Key Files                    |
| ------------ | -------------------- | ---------------- | ---------------------------- |
| MusicBrainz  | Album metadata lookup| REST API         | `musicbrainz_service.py`     |
| Cover Art Archive | Album covers    | HTTP URL         | Referenced in service (not directly called) |

**MusicBrainz Integration Details:**
- Base URL: `https://musicbrainz.org/ws/2`
- Endpoint: `/release` with query parameter `barcode:{barcode}`
- User-Agent: Required (set to "AlbumScanner/1.0 (jane42242002@gmail.com)")
- Timeout: 10 seconds
- Response: JSON with release information
- **Current Behavior**: Extracts title, artist, year, genre, cover_url but only title/artist are used

**Cover Art Archive:**
- URL Pattern: `https://coverartarchive.org/release/{release_id}/front`
- **Note**: URL is constructed but not validated or stored

### Internal Integration Points

- **Frontend Communication**: REST API on port 8000 (configurable via PORT env var)
- **Database**: SQLite (default) or PostgreSQL (via DATABASE_URL env var)
- **No Background Jobs**: All processing is synchronous
- **No Caching**: Every request hits database/external API

## Development and Deployment

### Local Development Setup

1. **Prerequisites**:
   - Python 3.x
   - pip

2. **Setup Steps**:
   ```bash
   pip install -r requirements.txt
   # Database is created automatically on first run
   ```

3. **Environment Variables** (optional):
   - `DATABASE_URL`: Database connection string (default: `sqlite:///./albums.db`)
   - `PORT`: Server port (default: 8000)

4. **Run Application**:
   ```bash
   # Direct execution
   python main.py
   
   # Or with uvicorn
   uvicorn main:app --reload
   ```

5. **Access**:
   - API: http://localhost:8000
   - Swagger Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/healthz

### Build and Deployment Process

- **No Build Step**: Python application, runs directly
- **Deployment**: 
  - Copy files to server
  - Install dependencies: `pip install -r requirements.txt`
  - Run: `uvicorn main:app --host 0.0.0.0 --port 8000`
- **Database**: 
  - SQLite: File-based, no setup needed
  - PostgreSQL: Requires database creation and migration (currently manual)
- **No CI/CD**: No automated deployment pipeline

### Known Setup Issues

- Alembic is in requirements but not configured (no `alembic.ini` or migrations directory)
- No `.env.example` file to document required environment variables
- Database file location not configurable (hardcoded to `./albums.db`)

## Testing Reality

### Current Test Coverage

- **Unit Tests**: None
- **Integration Tests**: None
- **E2E Tests**: None
- **Manual Testing**: Primary (and only) QA method

### Running Tests

```bash
# Tests don't exist, but if they did:
pytest           # Would run unit tests
pytest --cov     # Would run with coverage
```

**Note**: pytest is installed but no test files exist. This is a significant gap for a production application.

## Enhancement Impact Analysis

Based on the PRD enhancement requirements, these files will be affected:

### Files That Will Need Modification

**Story 1.1 - Data Model Extension:**
- `models.py` - Add year, genre, cover_url fields to Album model
- `schemas.py` - Update AlbumCreate, AlbumUpdate, AlbumOut schemas
- **NEW**: Alembic migration script (need to set up Alembic first)

**Story 1.2 - MusicBrainz Enhancement:**
- `musicbrainz_service.py` - Already extracts year/genre/cover_url, but need to ensure all cases handled
- `main.py` - Update `/api/search/barcode/{barcode}` endpoint response

**Story 1.3 - Barcode Scan Endpoint:**
- `main.py` - Add `POST /users/{user_id}/albums/scan` endpoint
- Reuse logic from existing `add_album` and MusicBrainz integration

**Story 1.4 - Advanced Search:**
- `main.py` - Enhance `GET /users/{user_id}/albums` endpoint
- Add query parameters: artist, year_min, year_max, genre
- Update database queries to support filtering
- May need new database indexes

**Story 1.5 - Image Recognition:**
- **NEW**: Image recognition service file (e.g., `image_recognition_service.py`)
- `main.py` - Add `POST /users/{user_id}/albums/recognize` endpoint
- Need to handle file uploads (FastAPI `UploadFile`)
- Integration with external image recognition API

**Story 1.6 - API Response Enhancement:**
- `schemas.py` - Update AlbumOut to include new fields
- `main.py` - All album-returning endpoints automatically updated (Pydantic handles it)

**Story 1.7 - Details Endpoint:**
- `main.py` - Add `GET /users/{user_id}/albums/{album_id}/details` endpoint
- May fetch additional info from MusicBrainz

### New Files/Modules Needed

1. **Alembic Setup**:
   - `alembic.ini` - Alembic configuration
   - `alembic/` directory - Migration scripts
   - First migration: Add year, genre, cover_url to albums table

2. **Image Recognition Service**:
   - New file: `image_recognition_service.py` (or similar)
   - Integrate with Google Vision API, AWS Rekognition, or similar
   - Handle image upload, processing, and result parsing

3. **Optional - Service Layer**:
   - Consider extracting business logic from `main.py` to service files
   - `album_service.py` - Album business logic
   - `search_service.py` - Search/filter logic

### Integration Considerations

- **Database Migrations**: Must set up Alembic before Story 1.1
- **Backward Compatibility**: All new fields must be nullable to not break existing data
- **API Compatibility**: Existing endpoints must continue to work (Pydantic will handle new fields gracefully)
- **MusicBrainz Rate Limits**: May need to implement caching or rate limiting
- **Image Upload**: Need to configure FastAPI for file uploads (multipart/form-data)
- **Error Handling**: Need consistent error handling across new endpoints
- **Logging**: Should add proper logging for new functionality

### Technical Constraints

1. **Must Maintain**: 
   - Existing API contract (backward compatible)
   - Existing data (no data loss)
   - Existing search functionality (title search)

2. **Must Follow**:
   - Current code patterns (route handlers in main.py)
   - Pydantic schema validation
   - SQLAlchemy ORM patterns
   - FastAPI dependency injection for database sessions

3. **Cannot Break**:
   - Existing duplicate checking logic
   - User-album relationship (CASCADE delete)
   - Unique constraints on normalized_title and barcode

## Appendix - Useful Commands and Scripts

### Frequently Used Commands

```bash
# Run application
python main.py
# or
uvicorn main:app --reload

# View database (utility script)
python view_db.py

# Install dependencies
pip install -r requirements.txt

# (Future) Run migrations (after Alembic setup)
alembic upgrade head

# (Future) Create migration
alembic revision --autogenerate -m "Add year genre cover_url to albums"
```

### Debugging and Troubleshooting

- **Logs**: Currently no logging - errors print to console
- **Database**: Use `view_db.py` to inspect database contents
- **API Testing**: Use Swagger UI at `/docs` endpoint
- **Common Issues**:
  - Database locked: SQLite doesn't handle concurrent writes well
  - MusicBrainz timeout: External API may be slow or unavailable
  - Port already in use: Change PORT environment variable

### Code Quality Notes

- **Type Hints**: Good coverage (uses Mapped, Optional, etc.)
- **Error Handling**: Basic (HTTPException with status codes)
- **Code Style**: Mixed (some tabs, some spaces - line 19-24 uses tabs)
- **Documentation**: Minimal (no docstrings on most functions)
- **Validation**: Good (Pydantic handles request/response validation)

