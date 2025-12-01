# Quick Reference - Key Files and Entry Points

## Critical Files for Understanding the System

- **Main Entry**: `main.py` - FastAPI application entry point
- **Configuration**: `database.py` - Database connection and session management
- **Core Business Logic**: `main.py` - All API endpoints and business logic
- **Data Models**: `models.py` - SQLAlchemy ORM models (User, Album)
- **API Schemas**: `schemas.py` - Pydantic request/response models
- **External Service**: `musicbrainz_service.py` - MusicBrainz API integration
- **Utilities**: `utils.py` - Title normalization helper

## Enhancement Impact Areas

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
