#!/usr/bin/env python
# coding=utf-8

import pandas as pd
from itertools import repeat

from connection import Connection
from utils import fix_int64


class Postgres():

    def __init__(self):
        pass

    def query(self, query, insertion=None, mode=['read', 'write']):
        with Connection() as cursor:
            cursor.execute(query, insertion)
            if mode == 'read':
                return cursor.fetchall()
        return

    def to_dataframe(self, columns, table, conditions=None):
        df = pd.DataFrame(columns=columns)
        columns = ', '.join(df.columns)

        if conditions:
            query = "SELECT {} FROM {} WHERE {};".format(
                columns, table, conditions)
        else:
            query = "SELECT {} FROM {};".format(columns, table)

        result = self.query(query, mode='read')
        for index, items in enumerate(result):
            df.loc[index] = items
        return df

    def from_dataframe(self, df, table):
        columns = ', '.join(df.columns)
        placeholder = ', '.join(repeat('%s', len(df.columns)))
        query = "INSERT INTO {} ({}) VALUES ({})".format(
            table, columns, placeholder)
        for row in df.itertuples():
            # Numpy.int64 is not supported by psycopg2 type conversion
            # row first element is the DataFrame index
            values = [fix_int64(el) for el in row[1:]]
            self.query(query, values, mode='write')
