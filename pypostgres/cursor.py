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
        self.pk = self.fetch(fetch_size) if values else None

    def __repr__(self):
        return '<Cursor (%s, %s)>' % (self.sql, self.values)

    def fetch(self, size=None):
        with self.connection as conn:
            with conn.cursor() as cursor:
                if self.values is not None:
                    if is_nested(self.values):
                        cursor.executemany(self.sql, self.values)
                    else:
                        cursor.execute(self.sql, self.values)
                else:
                    cursor.execute(self.sql)
                if size is not None:
                    if size in (1, 'one'):
                        return cursor.fetchone()
                    elif size in (0, '*', 'all'):
                        return cursor.fetchall()
                    elif isinstance(size, int):
                        return cursor.fetchmany(size)
                    return TypeError('Inappropriate size type: %s' % type(size))

    @property
    def all(self):
        return self.fetch(0)

    @property
    def one(self):
        return self.fetch(1)

    def many(self, size):
        return self.fetch(size)

    def commit(self):
        self.pk = self.fetch(self.fetch_size) if self.fetch_size else self.fetch()
