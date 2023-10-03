import psycopg2
from flask import Flask
from psycopg2 import sql

T_SCORES = "scores"


class DB:
    def __init__(self, app: Flask):
        self.app = app
        self.conn = None

    def connect(self):
        self.app.logger.info("Opening database connection")

        conf = self.app.config
        self.conn = psycopg2.connect(
            host=conf["DB_HOST"],
            database=conf["DB_DATABASE"],
            user=conf["DB_USER"],
            password=conf["DB_PASSWORD"],
        )

    def disconnect(self):
        self.app.logger.info("Closing database connection")

        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def get_all(self, table: str):
        with self.conn.cursor() as cur:
            cur.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table)))
            return cur.fetchall()

    def create(self, table: str, data: dict):
        key_string = ", ".join(["{}"] * len(data))
        value_string = ", ".join(["{}"] * len(data))
        query = sql.SQL(f"INSERT INTO {{}} ({key_string}) VALUES ({value_string})")
        values = (
            sql.Identifier(table),
            *(sql.Identifier(k) for k in data.keys()),
            *(sql.Literal(v) for v in data.values()),
        )
        with self.conn.cursor() as cur:
            cur.execute(query.format(*values), values)
            rowcount = cur.rowcount
        self.conn.commit()
        return rowcount
