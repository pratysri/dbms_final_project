-- PostgreSQL schema and seed data for DBMS Final Project

DROP TABLE IF EXISTS purchase_item CASCADE;
DROP TABLE IF EXISTS purchase CASCADE;
DROP TABLE IF EXISTS credit_card CASCADE;
DROP TABLE IF EXISTS product CASCADE;
DROP TABLE IF EXISTS customer CASCADE;

CREATE TABLE customer (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE credit_card (
  id SERIAL PRIMARY KEY,
  customer_id INTEGER NOT NULL REFERENCES customer(id) ON DELETE CASCADE,
  brand TEXT NOT NULL CHECK (brand IN ('Visa','Mastercard','Amex','Discover')),
  last4 CHAR(4) NOT NULL,
  exp_month SMALLINT CHECK (exp_month BETWEEN 1 AND 12),
  exp_year SMALLINT CHECK (exp_year >= EXTRACT(YEAR FROM now())),
  token TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE product (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  price NUMERIC(10,2) NOT NULL CHECK (price >= 0),
  stock_qty INTEGER NOT NULL CHECK (stock_qty >= 0),
  active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE purchase (
  id SERIAL PRIMARY KEY,
  customer_id INTEGER NOT NULL REFERENCES customer(id),
  purchased_at TIMESTAMPTZ DEFAULT now(),
  total_amount NUMERIC(12,2) NOT NULL CHECK (total_amount >= 0),
  status TEXT NOT NULL DEFAULT 'PAID' CHECK (status IN ('PAID','CANCELLED','REFUNDED'))
);

CREATE TABLE purchase_item (
  purchase_id INTEGER NOT NULL REFERENCES purchase(id) ON DELETE CASCADE,
  product_id INTEGER NOT NULL REFERENCES product(id),
  qty INTEGER NOT NULL CHECK (qty > 0),
  unit_price NUMERIC(10,2) NOT NULL CHECK (unit_price >= 0),
  PRIMARY KEY (purchase_id, product_id)
);

-- Helpful indexes
CREATE INDEX idx_product_active ON product(active);
CREATE INDEX idx_product_name ON product(name);
CREATE INDEX idx_cc_customer ON credit_card(customer_id);
CREATE INDEX idx_purchase_customer ON purchase(customer_id);

-- Seed data
INSERT INTO customer(name, email) VALUES
('Alice Johnson','alice@example.com'),
('Bob Smith','bob@example.com'),
('Carol Patel','carol@example.com'),
('David Nguyen','david@example.com');

INSERT INTO credit_card(customer_id, brand, last4, exp_month, exp_year, token) VALUES
(1,'Visa','1111',12, EXTRACT(YEAR FROM now())::int + 2, 'tok_visa_alice'),
(1,'Mastercard','2222',7, EXTRACT(YEAR FROM now())::int + 3, 'tok_mc_alice'),
(2,'Amex','3333',4, EXTRACT(YEAR FROM now())::int + 4, 'tok_amex_bob');

INSERT INTO product(name, description, price, stock_qty, active) VALUES
('Wireless Mouse','Ergonomic 2.4G mouse',19.99,100,TRUE),
('Mechanical Keyboard','Backlit, blue switches',79.99,50,TRUE),
('USB-C Cable','1m braided cable',9.49,200,TRUE),
('1080p Webcam','Full HD webcam with mic',49.00,20,TRUE),
('Laptop Stand','Aluminum adjustable stand',34.95,15,TRUE),
('Noise Cancelling Headphones','Over-ear ANC',129.99,12,TRUE),
('Portable SSD 1TB','USB-C NVMe',89.99,25,TRUE),
('Smart LED Bulb','E26, tunable white',12.99,150,TRUE),
('4K Monitor','27-inch UHD IPS',279.00,8,TRUE),
('Phone Charger','20W USB-C PD',14.99,120,TRUE);

-- Example purchase to demonstrate joins
-- Create a purchase for Alice (id=1)
WITH new_p AS (
  INSERT INTO purchase(customer_id, total_amount)
  VALUES (1, 19.99 + 79.99)
  RETURNING id
)
INSERT INTO purchase_item(purchase_id, product_id, qty, unit_price)
SELECT id, 1, 1, 19.99 FROM new_p
UNION ALL
SELECT id, 2, 1, 79.99 FROM new_p;

-- Reduce stock for the above items
UPDATE product SET stock_qty = stock_qty - 1 WHERE id IN (1,2);
