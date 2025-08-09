# DBMS Final Project Starter (PostgreSQL + FastAPI + Basic Frontend)

This starter kit matches your course requirements:
- PostgreSQL schema + seed data
- Required SQL queries
- Minimal FastAPI API (CRUD for products, customers, credit cards, purchases)
- Super simple HTML frontend calling the API

## Quick Start

### 1) Create & seed the database
```bash
createdb dbms_final
psql -d dbms_final -f sql/db.sql
```

### 2) Set environment and run the API
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Set DATABASE_URL (adjust user/password/host/port as needed)
export DATABASE_URL="postgresql://localhost/dbms_final"

# Run the server
uvicorn app:app --reload
```

The API will run on http://127.0.0.1:8000

### 3) Open the basic frontend
Open `frontend/index.html` in your browser. It expects the API at `http://127.0.0.1:8000`.

---

## Project Structure
```
dbms_final_starter/
  docs/
    requirements.md
    schema.md
    erd.dbml
  sql/
    db.sql
    queries.sql
  backend/
    app.py
    db.py
    requirements.txt
  frontend/
    index.html
    app.js
    styles.css
  README.md
```

## Deliverables mapping
- **Requirements (PDF)**: export `docs/requirements.md` as PDF
- **ER Diagram**: open `docs/erd.dbml` in dbdiagram.io and export the image/PDF
- **Relational Schema**: `docs/schema.md`
- **DB Implementation**: `sql/db.sql` (single SQL file with CREATE TABLE + INSERTs)
- **SQL Queries**: `sql/queries.sql`
- **Business Logic / Demo**: run the API and use the frontend to demo
- **Video**: record your screen running the queries and the app
```
