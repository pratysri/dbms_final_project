-- Required SQL queries (examples)

-- 1) Customers and products they bought where price > 100 (JOIN across tables)
SELECT c.name AS customer, p.name AS product, pi.unit_price
FROM customer c
JOIN purchase pu ON pu.customer_id = c.id
JOIN purchase_item pi ON pi.purchase_id = pu.id
JOIN product p ON p.id = pi.product_id
WHERE pi.unit_price > 100
ORDER BY c.name;

-- 2) Top 5 products by total revenue
SELECT p.id, p.name, SUM(pi.qty * pi.unit_price) AS revenue
FROM purchase_item pi
JOIN product p ON p.id = pi.product_id
GROUP BY p.id, p.name
ORDER BY revenue DESC
LIMIT 5;

-- 3) Orders by customer with total amounts
SELECT c.id AS customer_id, c.name, COUNT(pu.id) AS orders, COALESCE(SUM(pu.total_amount),0) AS total_spent
FROM customer c
LEFT JOIN purchase pu ON pu.customer_id = c.id
GROUP BY c.id, c.name
ORDER BY total_spent DESC;

-- 4) Products low on stock (threshold 5)
SELECT id, name, stock_qty
FROM product
WHERE stock_qty < 5
ORDER BY stock_qty ASC;

-- 5) Average price of items purchased per customer
SELECT c.id, c.name, ROUND(AVG(pi.unit_price),2) AS avg_item_price
FROM customer c
JOIN purchase pu ON pu.customer_id = c.id
JOIN purchase_item pi ON pi.purchase_id = pu.id
GROUP BY c.id, c.name
ORDER BY avg_item_price DESC;

-- 6) Product catalog (active only) constrained to a price range
-- Example range used here; replace 0 and 100 with parameters in your app
SELECT id, name, price
FROM product
WHERE active = TRUE AND price BETWEEN 0 AND 100
ORDER BY price ASC;

-- 7) Purchase detail with line items for a given purchase id (example: 1)
SELECT pu.id, pu.customer_id, pu.purchased_at, pu.total_amount, pu.status,
       p.name AS product_name, pi.qty, pi.unit_price
FROM purchase pu
JOIN purchase_item pi ON pi.purchase_id = pu.id
JOIN product p ON p.id = pi.product_id
WHERE pu.id = 1
ORDER BY p.name ASC;
