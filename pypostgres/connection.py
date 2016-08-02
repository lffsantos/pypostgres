#!/usr/bin/env python3
#
#   PyPostgres
#   Marcellus Amadeus
#

# third-party
import psycopg2 as pg


class Connection(object):

    def __init__(self, dsn=None, **kwargs):
        self.settings = kwargs
        self.dsn = dsn
        self.conn = None
        self.cursor = None

    def __enter__(self, *args):
        self.conn = pg.connect(self.dsn) if self.dsn else pg.connect(**self.settings)
        self.cursor = self.conn.cursor()
        return self.conn, self.cursor

    def __exit__(self, *args):
        try:
            self.conn.commit()
        except:
            self.conn.rollback()
            raise
        finally:
            self.cursor.close()
            self.conn.close()
