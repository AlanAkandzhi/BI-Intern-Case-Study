-- ============================================================
-- BI Intern Home Task
-- SQL Solutions
-- Candidate: Alan Akandzhi
-- ============================================================


-- ============================================================
-- TASK 2.1
-- Show the names of all customers from Sofia.
-- ============================================================

SELECT name
FROM customers
WHERE city = 'София';


-- ============================================================
-- TASK 2.2
-- Show the number of completed orders for every customer.
--
-- LEFT JOIN is used because the task asks for all customers,
-- including customers with zero completed orders.
-- ============================================================

SELECT
    c.name,
    COUNT(o.id) AS completed_orders
FROM customers c
LEFT JOIN orders o
    ON c.id = o.customer_id
    AND o.status = 'completed'
GROUP BY c.id, c.name
ORDER BY c.id;


-- ============================================================
-- TASK 2.2 - BONUS
-- Show completed orders and revenue for every customer.
--
-- DISTINCT prevents an order from being counted more than once
-- after joining it with multiple product rows.
-- ============================================================

SELECT
    c.name,
    COUNT(DISTINCT o.id) AS completed_orders,
    COALESCE(
        ROUND(SUM(p.quantity * p.unit_price), 2),
        0
    ) AS revenue
FROM customers c
LEFT JOIN orders o
    ON c.id = o.customer_id
    AND o.status = 'completed'
LEFT JOIN products p
    ON p.order_id = o.id
GROUP BY c.id, c.name
ORDER BY c.id;


-- ============================================================
-- TASK 2.3
-- Count unique customers who have made at least one order.
--
-- COUNT(*) after joining orders and products would count rows
-- produced by the JOIN, not unique customers.
-- ============================================================

SELECT
    COUNT(DISTINCT customer_id) AS unique_customers
FROM orders;


-- ============================================================
-- TASK 2.3 - ALTERNATIVE BUSINESS DEFINITION
-- Count unique customers with at least one completed order.
-- ============================================================

SELECT
    COUNT(DISTINCT customer_id) AS unique_completed_customers
FROM orders
WHERE status = 'completed';