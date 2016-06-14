import psycopg2 as pg


class Connection():

    def __init__(self, **kwargs):
        self.settings = kwargs
        self.conn = None
        self.cursor = None

    def __enter__(self, *args):
        self.conn = pg.connect(**self.settings)
        self.cursor = self.conn.cursor()
        return (self.conn, self.cursor)

    def __exit__(self, *args):
        try:
            self.conn.commit()
        except:
            self.conn.rollback()
            raise
        finally:
            self.cursor.close()
            self.conn.close()
