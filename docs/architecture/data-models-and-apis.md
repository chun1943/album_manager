# Data Models and APIs

## Data Models

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

## API Specifications

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
