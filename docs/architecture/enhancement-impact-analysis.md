# Enhancement Impact Analysis

Based on the PRD enhancement requirements, these files will be affected:

## Files That Will Need Modification

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

## New Files/Modules Needed

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

## Integration Considerations

- **Database Migrations**: Must set up Alembic before Story 1.1
- **Backward Compatibility**: All new fields must be nullable to not break existing data
- **API Compatibility**: Existing endpoints must continue to work (Pydantic will handle new fields gracefully)
- **MusicBrainz Rate Limits**: May need to implement caching or rate limiting
- **Image Upload**: Need to configure FastAPI for file uploads (multipart/form-data)
- **Error Handling**: Need consistent error handling across new endpoints
- **Logging**: Should add proper logging for new functionality

## Technical Constraints

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
