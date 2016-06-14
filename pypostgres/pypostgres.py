#!/usr/bin/env python
# coding=utf-8

import pandas as pd
from itertools import repeat

from pypostgres.connection import Connection
from pypostgres.utils import fix_int64
from pypostgres.utils import untuple


class Postgres():

    def __init__(self, dbname, username, password='', host='localhost', port=5432):
        self.settings = {
            'dbname': dbname,
            'username': username,
            'password': password,
            'host': host,
            'port': str(port)
        }

    def query(self, query, values=None, result=False):
        with Connection(**self.settings) as session:
            connection, cursor = session
            cursor.execute(query, values)
            if result:
                return cursor.fetchall()
        return

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

    def to_dataframe(self, table, columns='*', conditions=None):
        if columns == '*':
            columns = self.get_table_columns(table)
        
        flat_columns = ', '.join(columns)

        if not conditions:
            sql = "SELECT {} FROM {};".format(
                flat_columns, table)
        else:
            sql = "SELECT {} FROM {} WHERE {};".format(
                flat_columns, table, conditions)

        result = self.query(sql, result=True)
        return self.build_dataframe(result, columns)
        

    def from_dataframe(self, df, table):
        columns = ', '.join(df.columns)
        placeholder = ', '.join(repeat('%s', len(df.columns)))
        query = "INSERT INTO {} ({}) VALUES ({})".format(
            table, columns, placeholder)
        for row in df.itertuples():
            # Numpy.int64 is not supported by psycopg2 type conversion
            # row first element is the DataFrame index
            values = [fix_int64(el) for el in row[1:]]
            self.query(query, values)
