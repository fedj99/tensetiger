from logging import info

import psycopg2
from flask import current_app


class DB:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        info("Connecting to DB")

        conf = current_app.config
        self.conn = psycopg2.connect(
            host=conf["DB_HOST"],
            database=conf["DB_DATABASE"],
            user=conf["DB_USER"],
            password=conf["DB_PASSWORD"],
        )
        self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def get_all(self, table: str):
        self.cursor.execute(f"SELECT * FROM {table};")
        return self.cursor.fetchall()
