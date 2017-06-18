#!/usr/bin/env python3
from pypostgres.utils import is_nested


class Cursor(object):
    def __init__(self, connection, sql, values,
                 cursor_factory, fetch_size):
        self.connection = connection
        self.sql = sql
        self.values = values
        self.cursor_factory = cursor_factory
        self.fetch_size = fetch_size
        self.commit()

    def __repr__(self):
        return '<Cursor (%s, %s)>' % (self.sql, self.values)

    def commit(self):
        with self.connection as conn:
            with conn.cursor() as cursor:
                if self.values is not None:
                    if is_nested(self.values):
                        cursor.executemany(self.sql, self.values)
                    else:
                        cursor.execute(self.sql, self.values)
                if self.fetch_size is not None:
                    return self.fetch(self.fetch_size)

    def fetch(self, size, cursor):
        if size in (1, 'one'):
            return cursor.fetchone()
        elif size in (0, '*', 'all'):
            return cursor.fetchall()
        elif isinstance(size, int):
            return cursor.fetchmany(size)
        return TypeError('Inappropriate size type: %s' % type(size))

    @property
    def all(self):
        with self.connection as conn:
            with conn.cursor() as cursor:
                return self.fetch(0, cursor)

    @property
    def one(self):
        with self.connection as conn:
            with conn.cursor() as cursor:
                return self.fetch(1, cursor)

    def many(self, size):
        with self.connection as conn:
            with conn.cursor() as cursor:
                return self.fetch(size, cursor)
