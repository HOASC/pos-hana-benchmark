CREATE SCHEMA pos;
SET SCHEMA pos;

DROP TABLE transaction_items;
CREATE TABLE transaction_items (
        id INTEGER primary key
    ,   transaction_id INTEGER
    ,   item_id INTEGER
    ,   unit_price DECIMAL -- customer bought item at that price
    ,   unit_cost DECIMAL -- item cost retailer that much at that time
    ,   quantity INTEGER
);

DROP TABLE  transactions;
CREATE TABLE transactions (
        id INTEGER primary key
    ,   store_id INTEGER
    ,   customer_id INTEGER
    ,   type VARCHAR(20)
    ,   timestamp TIMESTAMP
);

DROP TABLE stores;
CREATE TABLE stores (
        id INTEGER primary key
    ,   name VARCHAR(30)
    ,   type VARCHAR(20)
    ,   address VARCHAR(50)
);

DROP TABLE customers;
CREATE TABLE customers (
        id INTEGER primary key
    ,   name VARCHAR(30)
);

DROP TABLE items;
CREATE TABLE items (
        id INTEGER primary key
    ,   name VARCHAR(50)
    ,   color VARCHAR(20)
    ,   size DECIMAL
    ,   category VARCHAR(30)
);