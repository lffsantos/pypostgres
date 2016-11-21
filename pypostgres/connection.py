#!/usr/bin/env python3

import psycopg2 as pg


class Connection(object):

    def __init__(self, **kwargs):
        self.settings = kwargs
        self.conn = None

    def __enter__(self, *args):
        self.conn = pg.connect(**self.settings)
        return self.conn

    def __exit__(self, *args):
        self.conn.close()
