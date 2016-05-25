import psycopg2 as pg


class Connection():

    def __init__(self, database, user, password=None, host='localhost', port=5432):
        self.config = {
            "dbname": database,
            "user": user,
            "password": password,
            "host": host,
            "port": port
        }

    def __enter__(self, *args):
        dsn = ("dbname={dbname} "
            "user={user} " 
            "password={password} " 
            "host={host} " 
            "port={port}").format_map(self.config)
        self.conn = pg.connect(dsn)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, *args):
        try:
            self.conn.commit()
        except:
            session.rollback()
            raise
        finally:
            self.cursor.close()
            self.conn.close()
