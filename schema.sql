CREATE SCHEMA pos;
SET SCHEMA pos;

DROP TABLE transaction_items;
CREATE COLUMN TABLE transaction_items (
        id INTEGER primary key
    ,   transaction_id INTEGER
    ,   item_id INTEGER
    ,   unit_price DECIMAL
    ,   unit_cost DECIMAL
    ,   quantity INTEGER
);

DROP TABLE transactions;
CREATE COLUMN TABLE transactions (
        id INTEGER primary key
    ,   store_id INTEGER
    ,   customer_id INTEGER
    ,   type VARCHAR(20)
    ,   timestamp TIMESTAMP
);

DROP TABLE stores;
CREATE COLUMN TABLE stores (
        id INTEGER primary key
    ,   name VARCHAR(30)
    ,   type VARCHAR(20)
    ,   address VARCHAR(50)
);

DROP TABLE customers;
CREATE COLUMN TABLE customers (
        id INTEGER primary key
    ,   name VARCHAR(30)
);

DROP TABLE items;
CREATE COLUMN TABLE items (
        id INTEGER primary key
    ,   name VARCHAR(50)
    ,   color VARCHAR(20)
    ,   size DECIMAL
    ,   category VARCHAR(30)
);

MERGE DELTA OF transaction_items;
MERGE DELTA OF transactions;
MERGE DELTA OF stores;
MERGE DELTA OF customers;
MERGE DELTA OF items;