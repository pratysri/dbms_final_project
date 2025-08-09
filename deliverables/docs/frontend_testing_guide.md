# Frontend Testing Guide

This guide walks you (or a grader) through testing the modern minimalist frontend against the FastAPI backend.

## Prerequisites
- API running at: http://127.0.0.1:8000 (Swagger UI: http://127.0.0.1:8000/docs)
- Frontend served at: http://127.0.0.1:8080
- Database seeded (see `sql/db.sql`).

If needed, quick start is in `README.md`.

## Open the app
- Visit: http://127.0.0.1:8080
- The Products list will auto-load from `GET /products`.

## Products: Search
1) In the Products card, fill:
   - Search name: `Wireless`
   - Min price: `5`
   - Max price: `20`
2) Click Search.
3) Expected: Filtered list in the Products area.

## Add Product
1) In Add Product, enter:
   - Name: `Desk Mat`
   - Description: `Felt 35x65cm`
   - Price: `16.99`
   - Stock Qty: `50`
2) Click Add.
3) Expected: Message “Product added ✔” and the new product appears in the Products list with an ID.

## Register Customer
1) In Register Customer, enter:
   - Full name: `Alice Johnson`
   - Email: `alice@example.com`
2) Click Register.
3) Expected: Message “Customer #<id> created ✔”. Note this customer ID.

## Create Purchase
1) In Create Purchase, enter:
   - Customer ID: use the ID from the previous step (e.g., `1`).
   - Items JSON: a valid JSON array of product/qty. Example:
   ```json
   [{"product_id": 1, "qty": 1}, {"product_id": 3, "qty": 2}]
   ```
   Tip: Use product IDs visible in the Products list.
2) Click Purchase.
3) Expected: “Purchase #<id> created: $<total>”. Note the purchase ID.

## Low Stock
1) In Low Stock, set Threshold (default 5): e.g., `10`.
2) Click Load.
3) Expected: List of products with stock below the threshold, or “No low-stock products”.

## Update Product
1) In Update Product, set:
   - Product ID: an existing product ID (e.g., the new Desk Mat ID).
   - Optional fields (fill only what you want to change):
     - Name (optional): `Desk Mat Pro`
     - Description (optional): `Felt 40x80cm`
     - New Price (optional): `18.49`
     - New Stock (optional): `60`
2) Click Update.
3) Expected: “Product #<id> updated ✔” and the Products list refreshes.

## Toggle Product Active
1) In Toggle Product Active, set:
   - Product ID: same ID as above.
   - Active: check (true) or uncheck (false).
2) Click Apply.
3) Expected: “Product #<id> active=<true|false> ✔” and the Products list updates accordingly.

## Purchase Detail
1) In Purchase Detail, enter:
   - Purchase ID: the ID returned by Create Purchase.
2) Click Fetch.
3) Expected in the Purchase Detail area:
   - Header with purchase id, customer_id, timestamp.
   - Total and status.
   - Items list with product name, qty, and unit price.

## Tips / Troubleshooting
- Use valid JSON in the Items JSON field (double quotes, not single). If invalid, the page will show “Invalid JSON”.
- If requests fail, check the API is running and reachable at http://127.0.0.1:8000.
- Endpoints are implemented in `backend/app.py`; the UI logic is in `frontend/app.js`.
