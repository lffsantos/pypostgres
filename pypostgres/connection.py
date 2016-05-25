import psycopg2 as pg
import settings


class Connection():

    def __init__(self):
        pass

    def __enter__(self, *args):
        self.conn = pg.connect(**settings.DATABASE)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, *args):
        try:
            self.conn.commit()
        except:
            self.conn.rollback()
            raise
        finally:
            self.cursor.close()
            self.conn.close()
