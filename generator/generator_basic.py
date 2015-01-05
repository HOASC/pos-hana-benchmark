#!/usr/bin/env python
# encoding: utf-8

import os, csv, re
from random import randint, paretovariate
from hanaConnector import HanaConnector

GENERATOR_PATH = os.path.join(os.path.dirname(__file__) + "/generated_data")
if not os.path.exists(GENERATOR_PATH):
    os.makedirs(GENERATOR_PATH)

db_config = {
    "address": "localhost",
    "port": 30115,
    "user": "SYSTEM",
    "password": "manager",
    "autocommit": True
}

con = HanaConnector(db_config)

def uniform(start, stop):
    return randint(start, stop)

def pareto(start, stop):
    return int(start - 1 + paretovariate(1.2))

# start stop is ignored. This will generate exactly THREE products!
def paretocontrolled(start, stop):
    rndnum = randint(1,100)
    if (rndnum <= 80):  # highly used product
        return 0
    elif (rndnum <= 95):  # medium used product
        return 1
    else:  # low used product
        return 2

DISTR_FUNC = { "uniform": uniform, "pareto": pareto, "paretocontrolled": paretocontrolled }


class Table(object):
    def __init__(self, name):
        self.name = name
        self.fields = []


class Field(object):
    def __init__(self, column_name):
        self.name = column_name


class TableGenerator(object):
    connection = con
    tablename = None

    def __init__(self, **options):
        self.table = None
        self.scale_factor = int(options["scale_factor"])
        self.num_records = self.scale_factor * self.tablename
        self.initialize_table()
        self.writer = FileWriter([f.name for f in self.table.fields])

    def generate(self):
        log.info("Working on %s with %s" % (self.tablename, self.scale_factor))
        self.generate_ctl_file()
        self.generate_csv_file(self.scale_factor)
        # if not self.generate_only:
        #     self.import_data()

    def initialize_table(self):
        # if self.table_exists():
        #     self.delete_table_content()

        self.table = Table(self.tablename)
        attr_list = self.connection.query_assoc('''SELECT
                                       COLUMN_NAME as "column_name"
                                  FROM "SYS"."COLUMNS"
                                  WHERE SCHEMA_NAME=:schema
                                  AND TABLE_NAME=:table
                                  ORDER BY POSITION''', schema=self.connection.schema, table=self.tablename.upper())
        assert attr_list, "Tables %s does not exist" % self.tablename
        for attr in attr_list:
            self.table.fields.append(Field(**attr))

    def table_exists(self):
        return True if (self.connection.query('''SELECT TABLE_NAME FROM SYS.TABLES
                                WHERE SCHEMA_NAME=:schema
                                AND TABLE_NAME=:table''' ,
                                schema=self.connection.schema,
                                table=self.tablename)) else False

    def drop_table(self):
        self.connection.execute("DROP TABLE %s" % self.tablename)
        log.info("Dropped table %s" % self.tablename)

    def create_table(self):
        self.connection.execute(self.table.print_create_statement())

    def delete_table_content(self):
        self.connection.execute('TRUNCATE TABLE %s' % self.tablename)

    @property
    def base_name(self):
        if not hasattr(self, '_basename'):
            self._basename = os.path.join(GENERATOR_PATH, "_".join([self.tablename.lower(), str(self.records)]))
        return self._basename

    @property
    def csv_fname(self):
         return self.base_name + ".csv"

    @property
    def ctl_fname(self):
        return self.base_name + ".ctl"

    def output_exists(self):
        return os.path.exists(self.csv_fname)

    def generate_ctl_file(self):
        log.info("Generating ctl file")
        with open(self.ctl_fname, 'w') as ctl_file:
            ctl = """IMPORT DATA INTO TABLE {table}
            FROM '{infile}'
            RECORD DELIMITED BY '\n'
            FIELD DELIMITED BY ','
            ERROR LOG '{badfile}'
            """.format(table=self.table.name,
                       infile=self.csv_fname,
                       badfile=self.tablename.lower() + '.bad')
            ctl_file.write(ctl)
            ctl_file.close()

    def save_row(self, row):
        self.writer.save_row(row, self.csv_fname)

    def generate_csv_file(self, scale_factor):
        log.info("Generating csv file")
        for row in self.generate_csv_rows(generate_csv_file):
            self.save_row(row)
        self.writer.close()

    def generate_csv_rows(self, num_records):
        pass

    def import_data(self):
        self.delete_table_content()
        log.info("Loading...")
        c = self.connection
        c.execute("IMPORT FROM '%s' WITH THREADS 10 BATCH 30000" % self.ctl_fname)
        log.info("Done")

class FileWriter(object):

    def __init__(self, fields):
        self.tables = {}
        self.handles = []
        self.fields = fields

    def save_row(self, row_dict, name):
        if not name in self.tables:
            csv_file = open(name, "w")
            self.handles.append(csv_file)
            self.tables[name] = csv.DictWriter(csv_file, self.fields, quoting=csv.QUOTE_NONE)
        self.tables[name].writerow(row_dict)

    def __del__(self):
        self.close()

    def close(self):
        for handle in self.handles:
            handle.close()