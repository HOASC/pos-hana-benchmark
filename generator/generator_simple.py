#!/usr/bin/env python
# encoding: utf-8

from random import randint, choice, paretovariate
from generator.generator_basic import TableGenerator, DISTR_FUNC


class CustomersGenerator(TableGenerator):
    """ Create data for customers

    Example data
    {
        'ID': 1,
        'NAME': 'customer 1'
    }
    """

    tablename = "Customers"
    default_size = 100

    def generate_csv_rows(self):
        for i in xrange(1, self.num_records):
            row = {
                    "ID": i,
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

    tablename = "Stores"
    default_size = 200

    TYPES = ['online', 'offline']

    def generate_csv_rows(self):
        for i in xrange(1, self.num_records):
            row = {
                    "ID": i,
                    'NAME': 'Store %s' % (i),
                    'TYPE': TYPES[randint(0, len(TYPES)-1)],
                    'ADDRESS': '%s 5th Avenue, 12345, New York City, NY' % (1234 + i)
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

    tablename = "Items"
    default_size = 500

    COLORS = ['white', 'yellow', 'orange', 'red', 'brown', 'green', 'blue', 'grey', 'purple', 'black']
    SIZES = range(1, 30)
    CATEGORIES = ['Jeans', 'Socks', 'TShirts', 'Shoes']

    def generate_csv_rows(self):
        for i in xrange(1, self.num_records):
            row = {
                    "ID": i,
                    'NAME': 'Item %s' % (i),
                    'COLOR': COLORS[randint(0, len(COLORS)-1)],
                    'SIZE': SIZES[randint(0, len(SIZES)-1)],
                    'CATEGORY': CATEGORIES[randint(0, len(CATEGORIES)-1)]
                  }
            yield row


# class FactGenerator(TableGenerator):
#     tablename = "Customers"

#     def generate_csv_rows(self, num_records):
#         for i in xrange(self.start_id, self.start_id + num_records):
#             row = {
#                     "ID": i,
#                     "DATE_": date,
#                     "PRODUCT": DISTR_FUNC[self.product_distribution](1, self.products + 1),
#                     "AMOUNT": randint(-9000, 10000),
#                   }
#             yield row


def generate(**options):
    # print options
    assert all(k in options for k in ("scale_factor")), "Specify records and other options"
    GENERATORS = [CustomersGenerator(**options), StoresGenerator(**options), ItemsGenerator(**options)]
    for generator in GENERATORS:
        generator.generate()