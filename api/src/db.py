import os

import click
import psycopg2
from flask import Flask, current_app, g
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

T_SCORES = "scores"
T_WORDS = "words"


def get():
    if "db" not in g or g.db.closed:
        # Create new connection
        conf = current_app.config
        g.db = psycopg2.connect(
            host=conf["DB_HOST"],
            database=conf["DB_DATABASE"],
            user=conf["DB_USER"],
            password=conf["DB_PASSWORD"],
        )

    return g.db


def cursor():
    db = get()

    if "db_cursor" not in g or g.db_cursor.closed:
        g.db_cursor = db.cursor(cursor_factory=RealDictCursor)

    return g.db_cursor


def close(e=None):
    db_cursor = g.pop("db_cursor", None)
    if db_cursor is not None:
        if not db_cursor.closed:
            db_cursor.close()

    db = g.pop("db", None)
    if db is not None:
        if not db.closed:
            db.close()


def init():
    db = get()

    # Get file directories
    migrations_dir = current_app.config["MIGRATIONS_DIR"]
    schema_dir = os.path.join(migrations_dir, "schema")
    data_dir = os.path.join(migrations_dir, "data")

    # Function to run all SQL files in a directory
    def run_all(base_dir):
        for dirpath, _dirnames, filenames in os.walk(base_dir):
            for fn in filenames:
                path = os.path.join(dirpath, fn)
                if not path.endswith(".sql"):
                    continue
                current_app.logger.info(f"Running migration: {path}")
                with current_app.open_resource(path, "r") as f:
                    with cursor() as cur:
                        cur.execute(f.read())
                    db.commit()

    # Create all schemas
    run_all(schema_dir)

    # Populate with data
    run_all(data_dir)


def get_all(table: str):
    with cursor() as cur:
        cur.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table)))
        return cur.fetchall()


def get_random_subset(table: str, subset_size: int):
    with cursor() as cur:
        cur.execute(
            sql.SQL("SELECT * FROM {} ORDER BY RANDOM() LIMIT {}").format(
                sql.Identifier(table), sql.Literal(subset_size)
            )
        )
        return cur.fetchall()


def create(table: str, data: dict):
    db = get()
    key_string = ", ".join(["{}"] * len(data))
    value_string = ", ".join(["{}"] * len(data))
    query = sql.SQL(f"INSERT INTO {{}} ({key_string}) VALUES ({value_string})")
    values = (
        sql.Identifier(table),
        *(sql.Identifier(k) for k in data.keys()),
        *(sql.Literal(v) for v in data.values()),
    )
    with cursor() as cur:
        cur.execute(query.format(*values), values)
        rowcount = cur.rowcount
    db.commit()
    return rowcount


@click.command("init-db")
def init_db_command():
    """Clear existing data and create new tables"""
    init()
    click.echo("Database initialized")


def init_app(app: Flask):
    app.teardown_appcontext(close)
    app.cli.add_command(init_db_command)
