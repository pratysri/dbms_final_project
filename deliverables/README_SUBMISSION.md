
## Contents
- docs/
  - requirements.pdf (from `docs/requirements.md`)
  - schema.pdf (from `docs/schema.md`)
  - frontend_testing_guide.pdf (from `docs/frontend_testing_guide.md`)
  - erd.dbml (source ERD)
  - ERD_EXPORT_INSTRUCTIONS.md (how to export ERD to PNG/PDF)
- sql/
  - db.sql (schema + seed)
  - queries.sql (7 example queries)

## How to run (quick)
1. Start PostgreSQL and create the DB:
   - `createdb dbms_final`
   - `psql -d dbms_final -f sql/db.sql`
2. Backend (FastAPI):
   - `cd backend`
   - `python3 -m venv .venv && source .venv/bin/activate`
   - `pip install -r requirements.txt`
   - `export DATABASE_URL=postgresql://localhost/dbms_final`
   - `uvicorn app:app --reload`
   - Swagger: http://127.0.0.1:8000/docs
3. Frontend:
   - Serve `frontend/` statically, e.g. `python3 -m http.server 8080` (run in the `frontend/` folder)
   - Open http://127.0.0.1:8080

## Notes
- All code remains in the project root (backend/, frontend/, sql/, docs/). This `deliverables/` folder collects the specific items needed for submission.
- If PDF export failed on your machine, HTML fallbacks may be generated instead; see docs/ or run the export script again with pandoc installed.
