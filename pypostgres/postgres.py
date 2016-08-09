#!/usr/bin/env python3
#
#   PyPostgres
#   Marcellus Amadeus
#

# third-party
import psycopg2 as pg

# local
from pypostgres.connection import Connection
from pypostgres.utils import is_nested
from pypostgres.utils import Error
from pypostgres.utils import Result


class Postgres(object):

    def __init__(self, database, user, password='', host='', port='', debug=False):
        self.settings = {
            "database": database,
            "user": user,
            "password": password,
            "host": host,
            "port": port
        }
        self.debug = debug

    def __repr__(self):
        return ("PostgreSQL: {user}@{host}:{port}\n"
                "Database: {database}"
                ).format(user=self.settings["user"],
                         host=self.settings["host"] if self.settings["host"] else 'localhost',
                         port=self.settings["port"] if self.settings["port"] else '5432',
                         database=self.settings["database"])

    def query(self, sql, values=None, fetch=1):
        with Connection(**self.settings) as (_, cursor):
            if self.debug:
                print(cursor.mogrify(sql, values))
            try:
                if values and is_nested(values):
                    cursor.executemany(sql, values)
                elif values:
                    cursor.execute(sql, values)
                else:
                    cursor.execute(sql)
            except Exception as e:
                return Result(False, Error(e, e.__class__.__name__))

            data = None
            if fetch is not None:
                try:
                    if fetch == 0 or fetch == 'all' or fetch == '*':
                        data = cursor.fetchall()
                    elif fetch == 1 or fetch == 'one':
                        data = cursor.fetchone()
                    elif isinstance(fetch, int):
                        data = cursor.fetchmany(fetch)
                except pg.ProgrammingError:
                    # there is nothing to fetch
                    pass
            if data:
                if len(list(data)) == 1:
                    data = data[0]
                elif is_nested(data) and all([len(row) == 1 for row in data]):
                    data = [row[0] for row in data]
            return Result(True, data)

    def get_table_columns(self, table):
        sql = "SELECT column_name FROM information_schema.columns WHERE table_name=%s;"
        result = self.query(sql, values=(table,), fetch='all')
        return result.response
