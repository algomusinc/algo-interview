import psycopg2


class Persistence(object):

    def __init__(self):
        self.connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            host="db",
            port=5432
        )
        self.connection.set_session(autocommit=True)

    def close(self):
        self.connection.close()
