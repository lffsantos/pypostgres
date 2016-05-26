#!/usr/bin/env python
# coding=utf-8

import pandas as pd
from itertools import repeat

from connection import Connection
from utils import fix_int64
from utils import untuple


class Postgres():

    def __init__(self, table=None):
        self.table = table
        self.columns = get_table_columns(self.table) if table else None

    def query(self, query, values=None, result=False):
        with Connection() as session:
            connection, cursor = session
            cursor.execute(query, values)
            if result:
                return cursor.fetchall()
        return

    @staticmethod
    def get_table_columns(table):
        sql = "select column_name from information_schema.columns where table_name='{}';"
        columns = self.query(sql.format(table), result=True)
        return untuple(columns)

    @staticmethod
    def build_dataframe(result_set, columns):
        df = pd.DataFrame(columns=columns)
        for index, items in enumerate(result):
            df.loc[index] = items
        return df

    def to_dataframe(self, table, columns='all', conditions=None):
        assert columns == 'all' or isinstance(columns, list)

        if columns == 'all':
            self.table = table
            columns = self.columns

        flat_columns = ', '.join(columns)

        if conditions:
            query = "SELECT {} FROM {} WHERE {};".format(
                flat_columns, table, conditions)
        else:
            query = "SELECT {} FROM {};".format(flat_columns, table)

        result = self.query(query, result=True)
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
