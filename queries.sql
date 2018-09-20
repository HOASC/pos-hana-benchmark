-- get customer stats
set schema POS;
CREATE VIEW customer_transactions AS (
    -- select all transaction items, group them up to get some transaction stats
    SELECT
        transaction_id
    ,   customer_id
    ,   timestamp
    ,   sum(price)    AS total
    ,   sum(quantity) AS item_count
    ,   max(price)    AS max_price
    FROM (
        -- pull out the fields we need
        SELECT
            transaction_items__quantity   AS quantity
        ,   transaction_items__id         AS id
        ,   transaction_items__price      AS price
        ,   transaction_items__unit_price AS unit_price
        ,   transaction_items__item_id    AS item_id
        ,   transactions__id              AS transaction_id
        ,   transactions__customer_id     AS customer_id
        ,   transactions__timestamp       AS timestamp
        FROM (
            SELECT
                transaction_items.quantity       AS transaction_items__quantity
            ,   transaction_items.unit_price     AS transaction_items__unit_price
            ,   transaction_items.id             AS transaction_items__id
            ,   transaction_items.price          AS transaction_items__price
            ,   transaction_items.item_id        AS transaction_items__item_id
            ,   transaction_items.transaction_id AS transaction_items__transaction_id
            ,   transactions.type                AS transactions__type
            ,   transactions.customer_id         AS transactions__customer_id
            ,   transactions.store_id            AS transactions__store_id
            ,   transactions.timestamp           AS transactions__timestamp
            ,   transactions.id                  AS transactions__id
            -- these are generated from the filters
            FROM (select transaction_items.id, transaction_items.transaction_id, transaction_items.item_id, transaction_items.quantity, ( unit_price ) as unit_price, ( (unit_price) * quantity ) as price from transaction_items) transaction_items
            JOIN (select transactions.* from transactions where transactions.type = 'instore') transactions
              ON transactions.id = transaction_items.transaction_id
        ) fact
    ) t
    GROUP BY
        transaction_id
    ,   timestamp
    ,   customer_id
);

SELECT
    *
    -- NOTE: I just picked arbitrary weights
,   ((rank_transaction_count * 0.20)
    +(rank_total_spent       * 0.20)
    +(rank_avg_spent         * 0.20)
    +(rank_total_item_count  * 0.20)
    +(rank_avg_max_price     * 0.20)
    ) AS rank_overall
FROM (
    SELECT
    -- NOTE: `percentage_rank` might be more appropriate, doesn't matter for testing
        *
    ,   cume_dist() OVER (ORDER BY t.transaction_count DESC) AS rank_transaction_count
    ,   cume_dist() OVER (ORDER BY t.total_item_count DESC)  AS rank_total_item_count
    ,   cume_dist() OVER (ORDER BY t.avg_spent DESC)         AS rank_avg_spent
    ,   cume_dist() OVER (ORDER BY t.total_spent DESC)       AS rank_total_spent
    ,   cume_dist() OVER (ORDER BY t.avg_max_price DESC)     AS rank_avg_max_price
    FROM (
        SELECT
            customer_id
        ,   count(transaction_id)      AS transaction_count
        ,   sum(item_count)            AS total_item_count
        ,   avg(item_count)            AS avg_item_count
        ,   sum(total)                 AS total_spent
        ,   avg(total)                 AS avg_spent
        ,   avg(max_price)             AS avg_max_price
        FROM customer_transactions
        GROUP BY
            customer_id
    ) t
) t;
