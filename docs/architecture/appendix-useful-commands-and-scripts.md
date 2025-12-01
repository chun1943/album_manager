# Appendix - Useful Commands and Scripts

## Frequently Used Commands

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

## Debugging and Troubleshooting

- **Logs**: Currently no logging - errors print to console
- **Database**: Use `view_db.py` to inspect database contents
- **API Testing**: Use Swagger UI at `/docs` endpoint
- **Common Issues**:
  - Database locked: SQLite doesn't handle concurrent writes well
  - MusicBrainz timeout: External API may be slow or unavailable
  - Port already in use: Change PORT environment variable

## Code Quality Notes

- **Type Hints**: Good coverage (uses Mapped, Optional, etc.)
- **Error Handling**: Basic (HTTPException with status codes)
- **Code Style**: Mixed (some tabs, some spaces - line 19-24 uses tabs)
- **Documentation**: Minimal (no docstrings on most functions)
- **Validation**: Good (Pydantic handles request/response validation)
