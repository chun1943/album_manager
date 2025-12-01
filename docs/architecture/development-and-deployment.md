# Development and Deployment

## Local Development Setup

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

## Build and Deployment Process

- **No Build Step**: Python application, runs directly
- **Deployment**: 
  - Copy files to server
  - Install dependencies: `pip install -r requirements.txt`
  - Run: `uvicorn main:app --host 0.0.0.0 --port 8000`
- **Database**: 
  - SQLite: File-based, no setup needed
  - PostgreSQL: Requires database creation and migration (currently manual)
- **No CI/CD**: No automated deployment pipeline

## Known Setup Issues

- Alembic is in requirements but not configured (no `alembic.ini` or migrations directory)
- No `.env.example` file to document required environment variables
- Database file location not configurable (hardcoded to `./albums.db`)
