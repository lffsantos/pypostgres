#!/usr/bin/env python3
#
#   PyPostgres
#   Marcellus Amadeus
#

# stdlib
from itertools import repeat

# third-party
import pandas as pd
import psycopg2 as pg

# local
from pypostgres.connection import Connection
from pypostgres.utils import fix_int64
from pypostgres.utils import is_nested
from pypostgres.utils import Error
from pypostgres.utils import Result


class Postgres():

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
            assert (values is None 
                    or isinstance(values, tuple)
                    or isinstance(values, list)), 'Invalid values type: {}'.format(type(values))
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
                    if fetch == 0 or fetch == 'all':
                        data = cursor.fetchall()
                    elif fetch == 1 or fetch == 'one':
                        data = cursor.fetchone()
                    elif isinstance(fetch, int):
                        data = cursor.fetchmany(fetch)
                except pg.ProgrammingError:
                    # there is nothing to fetch
                    pass
            if data:
                if (is_nested(data) and
                    all([len(row) == 1 for row in data])):
                    data = [row[0] for row in data]
                if len(data) == 1:
                    data = data[0]
            return Result(True, data)

    def get_table_columns(self, table):
        sql = "SELECT column_name FROM information_schema.columns WHERE table_name=%s;"
        result = self.query(sql, values=(table,), fetch='all')
        return result.response

    @staticmethod
    def build_dataframe(result_set, columns):
        df = pd.DataFrame(columns=columns)
        for index, items in enumerate(result_set):
            df.loc[index] = items
        return df

    def select_to_df(self, table, columns='*', conditions=None):
        if columns == '*':
            columns = self.get_table_columns(table)
        elif isinstance(columns, str):
            columns = [columns]
        
        flat_columns = ', '.join(columns)

        if not conditions:
            sql = "SELECT {} FROM {};".format(
                flat_columns, table)
        else:
            sql = "SELECT {} FROM {} WHERE {};".format(
                flat_columns, table, conditions)

        result = self.query(sql, fetch=0)
        if result.success:
            return self.build_dataframe(result.response, columns)
        else:
            raise result.response.exception
        
    def insert_from_df(self, df, table):
        columns = ', '.join(df.columns)
        placeholder = ', '.join(repeat('%s', len(df.columns)))
        query = "INSERT INTO {} ({}) VALUES ({})".format(
            table, columns, placeholder)
        for row in df.itertuples():
            # Numpy.int64 is not supported by psycopg2 type conversion
            # skipping row first element because it is the DataFrame index
            values = [fix_int64(el) for el in row[1:]]
            insertion = self.query(query, values)
            if not insertion.success:
                raise insertion.response.exception
        return Result(True, None)
