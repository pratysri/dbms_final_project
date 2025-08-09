# Relational Schema

## Tables

### customer
- id (PK, serial)
- name (text, NOT NULL)
- email (text, NOT NULL, UNIQUE)
- created_at (timestamptz, default now())

### credit_card
- id (PK, serial)
- customer_id (FK → customer.id, ON DELETE CASCADE)
- brand (text, NOT NULL, one of: Visa, Mastercard, Amex, Discover)
- last4 (char(4), NOT NULL)
- exp_month (smallint, 1–12)
- exp_year (smallint, >= current year)
- token (text, NOT NULL)
- created_at (timestamptz, default now())

### product
- id (PK, serial)
- name (text, NOT NULL)
- description (text)
- price (numeric(10,2), NOT NULL, >= 0)
- stock_qty (integer, NOT NULL, >= 0)
- active (boolean, default true)
- created_at (timestamptz, default now())

### purchase
- id (PK, serial)
- customer_id (FK → customer.id)
- purchased_at (timestamptz, default now())
- total_amount (numeric(12,2), NOT NULL, >= 0)
- status (text, default 'PAID', one of: PAID, CANCELLED, REFUNDED)

### purchase_item
- purchase_id (FK → purchase.id, ON DELETE CASCADE)
- product_id (FK → product.id)
- qty (integer, NOT NULL, > 0)
- unit_price (numeric(10,2), NOT NULL, >= 0)
- (PK: purchase_id, product_id)

## Notes
- `purchase_item.unit_price` captures the price at the time of purchase.
- Stock is reduced when a purchase is created.
- Indexes on foreign keys and frequent filters (product.name, product.active).
