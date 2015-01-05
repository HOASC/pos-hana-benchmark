#!/usr/bin/env python
# encoding: utf-8

from hdbcli import dbapi
import logging
from string import Template

class HanaConnector(object):

    def __init__(self, connection, schema="POS"):
        self.logger = logging.getLogger("HANA")
        self.connection = connection
        self.connect()
        if schema:
            self.set_schema(schema)

    def set_schema(self, schema):
        self.schema = schema
        self.execute("SET SCHEMA " + schema)

    def get_schema(self):
        return self.schema

    def connect(self):
        self.conn = dbapi.connect(**self.connection)
        self.cur = self.conn.cursor()

    def disconnect(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def __enter__(self):
        return self

    def __del__(self):
        self.disconnect()

    # ## Bare execution methods

    # The following methods don't yield results, thus should only be used when
    # no results are needed

    def commit(self):
        self.execute("COMMIT")

    def execute(self, query, *args, **kwargs):
        """
        Bare query execution. Results are available in `self.cur`.
        """
        # print query
        self.logger.debug(query)
        return self.cur.execute(query, *args, **kwargs)

    def execute_array(self, query_array, *args, **kwargs):
        for query in query_array:
            self.execute(query, args, **kwargs)

    def fetchall(self):
        return self.cur.fetchall()

    # ## Preferred database execution methods

    def query(self, query, *args, **kwargs):
        """
        Provide an easy interface for general query execution, returns a list
        of tuples.

        Usage::

            c = Connection(...)
            print c.query_assoc("SELECT FIRST_NAME, LAST_NAME FROM PEOPLE")
            [
                ("Peter", "Mueller"),
                ("Jenny", "Stichert")
                    ...
            ]
        """
        self.execute(query, *args, **kwargs)
        return self.cur.fetchall()

    def query_assoc(self, query, *args, **kwargs):
        """
        Provide an easy interface for general query execution that returns a
        list of dictionaries.

        Usage::

            c = Connection(...)
            print c.query_assoc("SELECT FIRST_NAME, LAST_NAME FROM PEOPLE")
            [
                {"FIRST_NAME": "Peter", "LAST_NAME": "Mueller"},
                {"FIRST_NAME": "Jenny", "LAST_NAME": "Stichert"},
                    ...
            ]
        """
        self.execute(query, *args, **kwargs)
        columns = [c[0] for c in self.cur.description]
        # turn results into dictionaries, so access is nicer
        results = []
        for line in self.cur.fetchall():
            results.append(dict(zip(columns, line)))
        return results

    def table_exists(self, table_name):
        self.execute("SELECT * FROM SYS.TABLES WHERE SCHEMA_NAME='%s' AND TABLE_NAME='%s'" % (self.schema, table_name.upper()))
        return len(self.fetchall()) == 1

    def delta_size(self, table_name):
        query_template = Template("SELECT RAW_RECORD_COUNT_IN_DELTA FROM \"SYS\".\"M_CS_TABLES\" WHERE TABLE_NAME = '$table_name' AND SCHEMA_NAME = '$schema_name' LIMIT 1")
        query_data = {"table_name": table_name.upper(), "schema_name": self.schema.upper()}
        self.execute(query_template.substitute(query_data))
        return self.fetchall()[0][0]

    def main_size(self, table_name):
        query_template = Template("SELECT RAW_RECORD_COUNT_IN_MAIN FROM \"SYS\".\"M_CS_TABLES\" WHERE TABLE_NAME = '$table_name' AND SCHEMA_NAME = '$schema_name' LIMIT 1")
        query_data = {"table_name": table_name.upper(), "schema_name": self.schema.upper()}
        self.execute(query_template.substitute(query_data))
        return self.fetchall()[0][0]

    def drop_table(self, table_name):
        if self.table_exists(table_name):
            self.execute("DROP TABLE %s" % table_name)

    def drop_view(self, view_name):
        self.execute("SELECT * FROM SYS.VIEWS WHERE SCHEMA_NAME='%s' AND VIEW_NAME='%s'" % (self.schema, view_name.upper()))
        view_exists = self.fetchall()
        if view_exists:
            self.execute("DROP VIEW %s" % view_name)

    def drop_procedure(self, procedure_name):
        self.execute("SELECT * FROM SYS.PROCEDURES WHERE SCHEMA_NAME='%s' AND PROCEDURE_NAME='%s'" % (self.schema, procedure_name.upper()))
        procedure_exists = self.fetchall()
        if procedure_exists:
            self.execute("DROP PROCEDURE %s" % procedure_name)

import unittest

class HanaConnectorTest(unittest.TestCase):

    def setUp(self):
        from config import Config
        database_config = Config.current()["database"]
        self.connection = HanaConnector(database_config)
        self.connection.execute("CREATE COLUMN TABLE testtest (id BIGINT primary key)")
        self.connection.execute("INSERT INTO testtest VALUES (1)")
        self.connection.execute("INSERT INTO testtest VALUES (2)")

    def test_delta_size_value(self):
        self.assertEqual(self.connection.delta_size("testtest"), 2)

    def test_delta_size_type(self):
        self.assertEqual(type(self.connection.delta_size("testtest")), int)

    def tearDown(self):
        self.connection.execute("DROP TABLE testtest")

def main():
	unittest.main()


if __name__ == "__main__":
	main()
