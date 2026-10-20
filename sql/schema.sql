PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    second_name TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('Заказчик', 'Исполнитель')),
    password TEXT NOT NULL,
    email TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    budget TEXT NOT NULL,
    customer_id INTEGER REFERENCES users(id),
    source_customer_id TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    executor_id INTEGER REFERENCES users(id),
    source_order_id TEXT NOT NULL,
    source_executor_id TEXT NOT NULL,
    comment TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    source_order_id TEXT NOT NULL,
    amount TEXT NOT NULL,
    status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    author_id INTEGER REFERENCES users(id),
    source_order_id TEXT NOT NULL,
    source_author_id TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    text TEXT NOT NULL DEFAULT ''
);
