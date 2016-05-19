#!/usr/bin/env python
# coding=utf-8

import psycopg2 as pg
import pandas as pd


class Connection():

    def __init__(self, db, user):
        self.db = db
        self.user = user

    def __enter__(self, *args):
        self.conn = pg.connect(
            "dbname={} user={}".format(self.db, self.user))
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, *args):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


class Postgres():

    def __init__(self, db, user='postgres'):
        self.db = db
        self.user = user

    def read(self, query):
        with Connection(self.db, self.user) as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def write(self, query, insertion=None):
        with Connection(self.db, self.user) as cursor:
            cursor.execute(query, insertion)

    def to_dataframe(self, columns, table, conditions=None):
        df = pd.DataFrame(columns=columns)
        columns = ', '.join(df.columns)
        result = self.read("SELECT {} FROM {};".format(columns, table))
        for index, items in enumerate(result):
            df.loc[index] = items
        return df
