#!/usr/bin/env python
# encoding: utf-8

from random import random, randint
from generator.generator_basic import TableGenerator
from datetime import datetime, timedelta

STORE_TYPES = ['online', 'instore']
COLORS = ['white', 'yellow', 'orange', 'red', 'brown', 'green', 'blue', 'grey', 'purple', 'black']
SIZES = range(1, 30)
CATEGORIES = ['Jeans', 'Socks', 'TShirts', 'Shoes']

DEFAULT_SIZES = {
    'customer': 100,
    'stores': 200,
    'items': 500,
    'transactions': 20000,
    'transaction_items': 100000
}


class TransactionsGenerator(TableGenerator):
    """ Create data for transactions

    Example data
    {
        'ID': 1,
        'STORE_ID': 1,
        'CUSTOMER_ID': 1,
        'TYPE': 'online',
        'TIMESTAMP': 'Jan 5, 2015 8:17:02.654 PM'
    }
    """

    tablename = "transactions"

    def generate_csv_rows(self):
        time_start = datetime.utcnow()-timedelta(weeks=10)
        num_stores = DEFAULT_SIZES['stores'] * self.scale_factor
        num_customers = DEFAULT_SIZES['customers'] * self.scale_factor
        for i in xrange(1, self.num_records + 1):
            row = {
                    'ID': i,
                    'STORE_ID': randint(1, num_stores),
                    'CUSTOMER_ID': randint(1, num_customers),
                    'TYPE': STORE_TYPES[randint(0, len(STORE_TYPES)-1)],
                    'TIMESTAMP': str(time_start+timedelta(seconds=i))
                  }
            yield row


class TransactionsItemsGenerator(TableGenerator):
    """ Create data for transactions items

    Example data
    {
        'ID': 1,
        'TRANSACTION_ID': 1,
        'ITEM_ID': 1,
        'UNIT_PRICE': 1.99,
        'UNIT_COST': 0.99,
        'QUANTITY': 5
    }
    """

    tablename = "transaction_items"

    def generate_csv_rows(self):
        self.num_transactions = DEFAULT_SIZES['transactions'] * self.scale_factor
        num_items = DEFAULT_SIZES['items'] * self.scale_factor
        counter = 1
        for i in xrange(1, self.num_transactions + 1):
            for j in xrange(1, randint(1, 10)):
                price = random() + randint(15, 50)
                row = {
                        'ID': counter,
                        'TRANSACTION_ID': i,
                        'ITEM_ID': randint(1, num_items),
                        'UNIT_PRICE': '%.2f' % price,
                        'UNIT_COST': '%.2f' % (price / ( 1 + (float(randint(5,25)) / 100))), # create a margin between 5% and 25%
                        'QUANTITY': randint(1, 5)
                      }
                counter += 1
                yield row


class CustomersGenerator(TableGenerator):
    """ Create data for customers

    Example data
    {
        'ID': 1,
        'NAME': 'customer 1'
    }
    """

    tablename = "customers"

    def generate_csv_rows(self):
        for i in xrange(1, self.num_records + 1):
            row = {
                    'ID': i,
                    'NAME': 'Customer %s' % (i)
                  }
            yield row


class StoresGenerator(TableGenerator):
    """ Create data for stores

    Example data
    {
        'ID': 1,
        'NAME': 'Store 1',
        'TYPE': 'online',
        'ADDRESS': '1234 5th Avenue'
    }
    """

    tablename = "stores"

    def generate_csv_rows(self):
        for i in xrange(1, self.num_records + 1):
            row = {
                    'ID': i,
                    'NAME': 'Store %s' % (i),
                    'TYPE': STORE_TYPES[randint(0, len(STORE_TYPES)-1)],
                    'ADDRESS': '%s 5th Avenue; 12345; New York City; NY' % (1234 + i)
                  }
            yield row


class ItemsGenerator(TableGenerator):
    """ Create data for items

    Example data
    {
        'ID': 1,
        'NAME': 'Item 1',
        'COLOR': 'red',
        'SIZE': '32'
        'CATEGORY': 'Jeans'
    }
    """

    tablename = "items"

    def generate_csv_rows(self):
        for i in xrange(1, self.num_records + 1):
            row = {
                    'ID': i,
                    'NAME': 'Item %s' % (i),
                    'COLOR': COLORS[randint(0, len(COLORS)-1)],
                    'SIZE': SIZES[randint(0, len(SIZES)-1)],
                    'CATEGORY': CATEGORIES[randint(0, len(CATEGORIES)-1)]
                  }
            yield row


def generate(**options):
    # print options
    GENERATORS = [CustomersGenerator(**options), StoresGenerator(**options), ItemsGenerator(**options), TransactionsGenerator(**options), TransactionsItemsGenerator(**options)]
    for generator in GENERATORS:
        generator.generate()