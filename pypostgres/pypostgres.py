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

    def query(self, query, insertion=None, mode=['read', 'write']):
        with Connection(self.db, self.user) as cursor:
            cursor.execute(query, insertion)
            if mode == 'read':
                return cursor.fetchall()
        return

    def to_dataframe(self, columns, table):
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
            self.write(query, insertion=row)
