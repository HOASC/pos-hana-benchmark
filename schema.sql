CREATE SCHEMA pos;
SET SCHEMA pos;

CREATE TABLE transaction_items (
        id INTEGER
    ,   transaction_id INTEGER
    ,   item_id INTEGER
    ,   unit_price DECIMAL -- customer bought item at that price
    ,   unit_cost DECIMAL -- item cost retailer that much at that time
    ,   quantity INTEGER
);

CREATE TABLE transactions (
        id INTEGER
    ,   store_id INTEGER
    ,   customer_id INTEGER
    ,   timestamp TIMESTAMP
);

CREATE TABLE stores (
        id INTEGER
    ,   name VARCHAR(30)
    ,   type VARCHAR(20)
    ,   address VARCHAR(50)
);

CREATE TABLE customers (
        id INTEGER
    ,   name VARCHAR(30)
);

CREATE TABLE items (
        id INTEGER
    ,   name VARCHAR(50)
    ,   color VARCHAR(20)
    ,   size DECIMAL
    ,   category VARCHAR(30)
);