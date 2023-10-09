from datetime import datetime
from urllib.parse import quote

from flask import Blueprint, jsonify, request, session
from psycopg2 import IntegrityError, sql
from werkzeug.security import check_password_hash, generate_password_hash

from api import db

bp = Blueprint("auth", __name__)


@bp.post("/register")
def register():
    username = request.json["username"]
    password = request.json["password"]

    if not username:
        return "Username not provided", 400
    if not password:
        return "Password not provided", 400

    with db.cursor() as cur:
        try:
            query = sql.SQL(
                "INSERT INTO {table} (username, password) VALUES (%s, %s) RETURNING id"
            ).format(table=db.T_USERS)
            cur.execute(query, (username, generate_password_hash(password)))
            user_id = cur.fetchone()["id"]
            db.commit()
        except IntegrityError:
            return f'User "{username}" is already taken', 400

    # User created, return to client
    user = db.find_by_id(db.T_USERS, user_id)

    return jsonify(user)


@bp.post("/login")
def login():
    username = request.json["username"]
    password = request.json["password"]

    if not username:
        return "Username not provided", 400
    if not password:
        return "Password not provided", 400

    user = db.find_by(db.T_USERS, "username", username, single=True)
    if user is None:
        return f'No such user: "{username}"'

    elif not check_password_hash(user["password"], password):
        return "Incorrect password"

    db.update(db.T_USERS, user["id"], {"last_logon": datetime.now().isoformat()})
    session.clear()
    session["user_id"] = user["id"]
    session["username"] = user["username"]

    return jsonify({"success": True, "user": user})
