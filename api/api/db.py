import os
from typing import Any

import click
import psycopg2
from flask import Flask, current_app, g
from psycopg2 import OperationalError, sql
from psycopg2.extras import RealDictCursor
from tabulate import tabulate

T_SCORES = "scores"
T_WORDS = "words"
T_USERS = "users"

### BOOTSTRAPPING


def get():
    if "db" not in g or g.db.closed:
        # Create new connection
        conf = current_app.config
        db_conf = dict(
            host=conf["DB_HOST"],
            database=conf["DB_DATABASE"],
            user=conf["DB_USER"],
            password=conf["DB_PASSWORD"],
        )
        current_app.logger.info("Connecting to database with:", db_conf)
        try:
            g.db = psycopg2.connect(**db_conf)
        except OperationalError as e:
            current_app.logger.error("Failed to connect to database!")
            current_app.logger.error(e)

    return g.db


def cursor():
    db = get()

    if "db_cursor" not in g or g.db_cursor.closed:
        g.db_cursor = db.cursor(cursor_factory=RealDictCursor)

    return g.db_cursor


def commit():
    db = get()
    db.commit()


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
    migrations_dir = os.path.realpath(
        os.path.join(current_app.root_path, current_app.config["MIGRATIONS_DIR"])
    )
    schema_dir = os.path.join(migrations_dir, "schema")
    data_dir = os.path.join(migrations_dir, "data")

    print(
        tabulate(
            [
                ["Working Directory", os.getcwd()],
                ["Application Root Path", current_app.root_path],
                ["Migrations Directory", migrations_dir],
            ],
            tablefmt="psql",
        )
    )

    # Function to run all SQL files in a directory
    def run_all(base_dir):
        paths = []
        if base_dir[0] != "/":
            base_dir = os.path.join(current_app.root_path, base_dir)
        for dirpath, _dirnames, filenames in os.walk(base_dir):
            for fn in filenames:
                path = os.path.join(dirpath, fn)
                if not path.endswith(".sql"):
                    continue
                paths.append(path)

        print("Found migrations:")
        print(*paths, sep="\n")
        ans = input("Continue? [y/N] ")
        if not ans.lower().startswith("y"):
            print("Aborting...")
            return
        for path in paths:
            current_app.logger.info(f"Running migration: {path}")
            with current_app.open_resource(path, "r") as f:
                with cursor() as cur:
                    cur.execute(f.read())
                db.commit()

    # Create all schemas
    run_all(schema_dir)

    # Populate with data
    run_all(data_dir)


### DATABASE METHODS


def get_all(table: str):
    with cursor() as cur:
        cur.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table)))
        return cur.fetchall()


def find_by(table: str, column: str, value: Any, operator: str = "=", single: bool = False):
    db = get()
    query = sql.SQL(f"SELECT * FROM {{table}} WHERE {{k}} {operator} %(value)s").format(
        table=sql.Identifier(table), k=sql.Identifier(column)
    )
    with cursor() as cur:
        cur.execute(query, {"value": value})
        if single:
            result = cur.fetchall()
            if cur.rowcount > 1:
                raise ValueError(
                    f"Requested single instance but found many in table `{table}`, looking for "
                    f"`{column}`{operator}{repr(value)}"
                )
            if len(result) == 0:
                return None
            return result[0]
        return cur.fetchall()


def find_by_id(table: str, id: Any):
    return find_by(table, "id", id, single=True)


def get_random_subset(table: str, subset_size: int):
    with cursor() as cur:
        cur.execute(
            sql.SQL("SELECT * FROM {} ORDER BY RANDOM() LIMIT {}").format(
                sql.Identifier(table), sql.Literal(subset_size)
            )
        )
        return cur.fetchall()


def get_top_k(table: str, orderby: str, k: int):
    query = sql.SQL("SELECT * FROM {table} ORDER BY {orderby} DESC LIMIT %(k)s").format(
        table=sql.Identifier(table), orderby=sql.Identifier(orderby)
    )
    with cursor() as cur:
        cur.execute(query, {"k": k})
        return cur.fetchall()


def get_top_k_filtered(table: str, orderby: str, filter_col: str, filter_val: str, k: int):
    query = sql.SQL(
        "SELECT * FROM {table} WHERE {filter_col} = %(filter_val)s ORDER BY {orderby} DESC LIMIT %(k)s"
    ).format(
        table=sql.Identifier(table),
        filter_col=sql.Identifier(filter_col),
        orderby=sql.Identifier(orderby),
    )
    with cursor() as cur:
        cur.execute(query, {"filter_val": filter_val, "k": k})
        return cur.fetchall()


def get_max(table: str, orderby: str, filter_col: str, filter_val: str):
    res = get_top_k_filtered(table, orderby, filter_col, filter_val, 1)
    if len(res) > 0:
        return res[0]
    return None


def create(table: str, data: dict):
    db = get()
    key_string = ", ".join(["{}"] * len(data))
    value_string = ", ".join(["{}"] * len(data))
    query = sql.SQL(f"INSERT INTO {{}} ({key_string}) VALUES ({value_string}) RETURNING id")
    values = (
        sql.Identifier(table),
        *(sql.Identifier(k) for k in data.keys()),
        *(sql.Literal(v) for v in data.values()),
    )
    with cursor() as cur:
        cur.execute(query.format(*values), values)
        new_id = cur.fetchone()["id"]
    db.commit()
    return new_id


def update(table: str, id: str | int, data: dict):
    data_keys = data.keys()
    update_sql = sql.SQL(", ".join(f"{{}}=%({k})s" for k in data_keys)).format(
        *[sql.Identifier(k) for k in data_keys]
    )
    query = sql.SQL('UPDATE {table} SET {update} WHERE "id"=%(id)s').format(
        table=sql.Identifier(table), update=update_sql
    )
    db = get()
    with cursor() as cur:
        cur.execute(query, {**data, "id": id})
        row_count = cur.rowcount
    db.commit()
    return row_count


### CLI


@click.command("init-db")
def init_db_command():
    """Clear existing data and create new tables"""
    init()
    click.echo("Database initialized")


def init_app(app: Flask):
    app.teardown_appcontext(close)
    app.cli.add_command(init_db_command)
