#!/usr/bin/env python3
import logging

from pypostgres.connection import Connection
from pypostgres.cursor import Cursor
from pypostgres.utils import get_cursor_factory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Postgres(object):
    def __init__(self, **kwargs):
        self.settings = kwargs

    def mogrify(self, sql, values):
        with Connection(**self.settings) as conn:
            with conn.cursor() as cursor:
                return cursor.mogrify(sql, values)

    def query(self, sql, values=None, cursor_factory=None, fetch_size=None):
        factory = get_cursor_factory(cursor_factory)
        logger.info('Query: "%s"' % self.mogrify(sql, values))
        return Cursor(Connection(**self.settings),
                      sql, values, factory, fetch_size)

    def get_columns(self, table, cursor_factory=None):
        sql = ("SELECT column_name FROM information_schema.columns "
               "WHERE table_name=%s;")
        cursor = self.query(sql, values=(table,),
                            cursor_factory=cursor_factory)
        return cursor.all

    def get_tables(self, cursor_factory=None):
        sql = "SELECT * FROM pg_catalog.pg_tables WHERE schemaname='public';"
        cursor = self.query(sql, cursor_factory=cursor_factory)
        return cursor.all

    def get_databases(self, cursor_factory=None):
        sql = "SELECT datname FROM pg_database WHERE datistemplate = false;"
        cursor = self.query(sql, cursor_factory=cursor_factory)
        return cursor.all
