#!/usr/bin/env python3

from pypostgres.utils import is_nested


class Cursor(object):
    '''The Cursor object only holds the information about the query
    only doing the actual request to db when fetching data except when
    values are passed
    '''

    def __init__(self, connection, sql, values, cursor_factory):
        self.connection = connection
        self.sql = sql
        self.values = values
        self.cursor_factory = cursor_factory
        if self.values:
            # passing values means insertion therefore
            # there is no need to wait until fetch
            self.fetch()

    def fetch(self, size=None):
        '''Execute SQL statements given (alongside optional values) and fetch the result

        :param size: fetch size, None (default) means there is not need to fetch anything
        :type size: int or None (default)
        '''
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
