-- name: users_list
SELECT id, name, second_name, role, email FROM users ORDER BY id;

-- name: orders_list
SELECT o.*, u.name AS customer_name, u.second_name AS customer_second_name
FROM orders AS o LEFT JOIN users AS u ON u.id = o.customer_id ORDER BY o.id;

-- name: applications_list
SELECT a.*, o.name AS order_name, u.name AS executor_name,
u.second_name AS executor_second_name
FROM applications AS a LEFT JOIN orders AS o ON o.id = a.order_id
LEFT JOIN users AS u ON u.id = a.executor_id ORDER BY a.id;

-- name: transactions_list
SELECT t.*, o.name AS order_name FROM transactions AS t
LEFT JOIN orders AS o ON o.id = t.order_id ORDER BY t.id;

-- name: reviews_list
SELECT r.*, o.name AS order_name, u.name AS author_name
FROM reviews AS r LEFT JOIN orders AS o ON o.id = r.order_id
LEFT JOIN users AS u ON u.id = r.author_id ORDER BY r.id;

-- name: user_by_id
SELECT id, name, second_name, role, email FROM users WHERE id = ?;

-- name: order_by_id
SELECT o.*, u.name AS customer_name, u.second_name AS customer_second_name
FROM orders AS o LEFT JOIN users AS u ON u.id = o.customer_id WHERE o.id = ?;

-- name: application_by_id
SELECT a.*, o.name AS order_name, u.name AS executor_name,
u.second_name AS executor_second_name
FROM applications AS a LEFT JOIN orders AS o ON o.id = a.order_id
LEFT JOIN users AS u ON u.id = a.executor_id WHERE a.id = ?;

-- name: transaction_by_id
SELECT t.*, o.name AS order_name FROM transactions AS t
LEFT JOIN orders AS o ON o.id = t.order_id WHERE t.id = ?;

-- name: review_by_id
SELECT r.*, o.name AS order_name, u.name AS author_name
FROM reviews AS r LEFT JOIN orders AS o ON o.id = r.order_id
LEFT JOIN users AS u ON u.id = r.author_id WHERE r.id = ?;

-- name: open_orders_search
SELECT o.*, u.name AS customer_name, u.second_name AS customer_second_name
FROM orders AS o LEFT JOIN users AS u ON u.id = o.customer_id
WHERE o.status = 'new' AND o.name LIKE ? ESCAPE '\' ORDER BY o.id;

-- name: orders_count
SELECT COUNT(*) AS total FROM orders;

-- name: applications_count
SELECT COUNT(*) AS total FROM applications;

-- name: orders_by_status
SELECT status, COUNT(*) AS total FROM orders GROUP BY status ORDER BY status;

-- name: applications_by_order
SELECT o.id, o.name, COUNT(a.id) AS total FROM orders AS o
LEFT JOIN applications AS a ON a.order_id = o.id
GROUP BY o.id, o.name ORDER BY o.id;

-- name: payments_by_order
SELECT o.id, o.name, COUNT(t.id) AS payment_count,
COALESCE(SUM(CAST(t.amount AS REAL)), 0) AS amount_total
FROM orders AS o LEFT JOIN transactions AS t ON t.order_id = o.id
GROUP BY o.id, o.name ORDER BY o.id;
