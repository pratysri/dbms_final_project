# DBMS Final Project

I completed a small e‑commerce system using PostgreSQL, FastAPI, and a minimalist vanilla JS frontend. This repository contains the runnable code plus a `deliverables/` folder with the PDFs and ERD for grading.

Highlights:
- Products, customers, credit cards, and purchases with line items
- Clean REST API (FastAPI) with Pydantic validation
- Minimal, modern UI (Pico.css) that exercises all endpoints
- SQL schema with seed data + example analytical queries

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

### 3) Run the frontend
From the `frontend/` directory, serve the files and open the app:
```bash
cd ../frontend
python3 -m http.server 8080
# then open http://127.0.0.1:8080
```

---

## Project Structure
```
dbms_final_starter/
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
  deliverables/
    docs/
      requirements.pdf
      schema.pdf
      frontend_testing_guide.pdf (or .md)
      ERD Diagram.png (or .pdf)
    sql/
      db.sql
      queries.sql
  README.md
```

## Deliverables (what I’m submitting)
- Requirements (PDF): `deliverables/docs/requirements.pdf`
- Relational schema (PDF): `deliverables/docs/schema.pdf`
- Frontend testing guide (PDF): `deliverables/docs/frontend_testing_guide.pdf` (or `.md`)
- ERD image: `deliverables/docs/ERD Diagram.png` (or `.pdf`)
- Database implementation: `deliverables/sql/db.sql` (CREATE TABLE + INSERT seed)
- Example SQL queries: `deliverables/sql/queries.sql`
- Submission readme: `deliverables/README_SUBMISSION.md`

## Basic Use Cases (what to try)
- Search products by name and price range
- Add a product, then verify it appears in the list
- Register a new customer
- Create a purchase with multiple line items (stock is validated and decremented)
- View purchase details (items, totals)
- Get low‑stock products below a threshold
- Update a product (name/description/price/stock)
- Toggle product active/inactive

See `deliverables/docs/frontend_testing_guide.pdf` for a step‑by‑step walkthrough with inputs to type.

## API Endpoints (summary)
- GET `/products` (with optional filters `name`, `min_price`, `max_price`)
- POST `/products`
- PUT `/products/{id}`
- PATCH `/products/{id}/active` (toggle active flag)
- GET `/products/low_stock?threshold=<n>`
- POST `/customers`
- GET `/customers/{id}/credit_cards`
- POST `/purchases` (creates purchase with items, validates stock)
- GET `/purchases/{id}` (detail with line items)

## Running the example SQL
You can execute example queries in `sql/queries.sql`:
```bash
psql -d dbms_final -f sql/queries.sql
```
Or copy/paste individual queries into `psql`.
