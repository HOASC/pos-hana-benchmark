#!/usr/bin/env python
# encoding: utf-8

from time import time
from hanaConnector import HanaConnector

db_config = {
    "address": "localhost",
    "port": 30515,
    "user": "",
    "password": "",
    "autocommit": True
}

RUNS = 10

connection = HanaConnector(db_config)

query = """
    SELECT
        *
    ,   ((rank_transaction_count * 0.20)
        +(rank_total_spent       * 0.20)
        +(rank_avg_spent         * 0.20)
        +(rank_total_item_count  * 0.20)
        +(rank_avg_max_price     * 0.20)
        ) AS rank_overall
    FROM (
        SELECT
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
    ) t"""

def run():
    runtimes = []

    print 'Starting Benchmark'
    for i in xrange(RUNS):
        t_start = time()
        connection.execute(query)
        t_end = time()
        runtimes.append( t_end - t_start )

    runtimes.sort()

    print runtimes
    print "Average Time: %f" % (sum(runtimes) / len(runtimes))


if __name__ == '__main__':
    run()

