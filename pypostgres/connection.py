#!/usr/bin/env python3
import logging
import psycopg2 as pg

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Connection(object):
    def __init__(self, **kwargs):
        self.settings = kwargs
        self.conn = None

    def __enter__(self, *args):
        self.conn = pg.connect(**self.settings)
        return self.conn

    def __exit__(self, *args):
        self.commit()

    def commit(self):
        try:
            self.conn.commit()
        except Exception as e:
            logger.exception(e)
            self.conn.rollback()
        finally:
            self.conn.close()
