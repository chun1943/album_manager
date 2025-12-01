# Source Tree and Module Organization

## Project Structure (Actual)

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

## Key Modules and Their Purpose

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
