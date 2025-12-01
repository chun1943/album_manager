# Technical Debt and Known Issues

## Critical Technical Debt

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

## Workarounds and Gotchas

- **Duplicate User Creation**: If username exists, returns existing user instead of error (line 36-37 in main.py)
- **Title Normalization**: Must use `normalize_title()` consistently for search to work
- **Barcode Search**: MusicBrainz service already returns year/genre/cover_url but they're not stored
- **Session Management**: Uses `autoflush=False, autocommit=False` - must explicitly commit
- **SQLite Thread Safety**: `check_same_thread=False` is set for SQLite (required for FastAPI)
