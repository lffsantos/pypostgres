#!/usr/bin/env python3

from pypostgres.utils import is_nested


class Cursor(object):

    def __init__(self, connection, sql, values, cursor_factory):
        self.connection = connection
        self.sql = sql
        self.values = values
        self.cursor_factory = cursor_factory

    def fetch(self, size=None):
        with self.connection as conn:
            with conn.cursor(cursor_factory=self.cursor_factory) as cursor:
                if self.values and is_nested(self.values):
                    cursor.executemany(self.sql, self.values)
                elif self.values:
                    cursor.execute(self.sql, self.values)
                else:
                    cursor.execute(self.sql)
                if size is not None:
                    if size in [1, 'one']:
                        return cursor.fetchone()
                    elif size in [0, '*', 'all']:
                        return cursor.fetchall()
                    else:
                        return cursor.fetchmany(size)

    @property
    def all(self):
        return self.fetch(0)

    @property
    def one(self):
        return self.fetch(1)

    def many(self, size):
        return self.fetch(size)
