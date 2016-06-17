#!/usr/bin/env python
# coding=utf-8

from itertools import repeat

import pandas as pd

from pypostgres.connection import Connection
from pypostgres.utils import fix_int64, untuple
from pypostgres.utils import Result, Error


class Postgres():

    def __init__(self, database, user, password='', host='', port=''):
        self.settings = {
            "database": database, 
            "user": user, 
            "password": password, 
            "host": host, 
            "port": port
        }

    def query(self, query, values=None):
        with Connection(**self.settings) as (conn, cursor):
            try:
                cursor.execute(query, values)
            except Exception as e:
                return Result(False, Error(e, e.__class__.__name__, repr(e)))
            else:
                data = None
                if query.upper().startswith('SELECT'):
                    data = cursor.fetchall()
                return Result(True, data)

    def get_table_columns(self, table):
        sql = "select column_name from information_schema.columns where table_name='{}';"
        columns = self.query(sql.format(table), result=True)
        return untuple(columns)

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

        result = self.query(sql)
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
