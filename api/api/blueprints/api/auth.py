from datetime import datetime
from functools import wraps
from urllib.parse import quote

from flask import Blueprint, g, jsonify, request, session
from psycopg2 import IntegrityError, sql
from werkzeug.security import check_password_hash, generate_password_hash

from api import db

bp = Blueprint("auth", __name__)


def require_login(route):
    @wraps(route)
    def decorator(*args, **kwargs):
        if g.user is None:
            return jsonify("Authorization required"), 401
        return route(*args, **kwargs)

    return decorator


@bp.post("/register")
def register():
    username = request.json.get("username")
    password = request.json.get("password")

    if not username:
        return jsonify("Username not provided"), 400
    if not password:
        return jsonify("Password not provided"), 400

    with db.cursor() as cur:
        try:
            query = sql.SQL(
                'INSERT INTO {table} (username, "password") VALUES (%s, %s) RETURNING id'
            ).format(table=sql.Identifier(db.T_USERS))
            cur.execute(query, (username, generate_password_hash(password)))
            user_id = cur.fetchone()["id"]
            db.commit()
        except IntegrityError:
            return f'User "{username}" is already taken', 400

    # Immediately perform login
    login()

    # User created, return to client
    user = db.find_by_id(db.T_USERS, user_id)

    return jsonify({"success": True, "user": user, "login_type": "new_user"})


@bp.post("/login")
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    if not username:
        return jsonify("Username not provided"), 400
    if not password:
        return jsonify("Password not provided"), 400

    user = db.find_by(db.T_USERS, "username", username, single=True)
    if user is None:
        # If there is no user with given username, create a new user with the given password
        g.login_type = "new_user"
        return register()

    # Login user
    elif not check_password_hash(user["password"], password):
        return jsonify("Incorrect password"), 401

    g.login_type = "existing_user"
    db.update(db.T_USERS, user["id"], {"last_logon": datetime.now().isoformat()})
    session.clear()
    session["user_id"] = user["id"]
    session["username"] = user["username"]

    # Create response
    res = jsonify({"success": True, "user": user, "login_type": g.login_type})
    # Set cookies
    res.set_cookie("user_id", quote(str(user["id"])), samesite="Lax")
    res.set_cookie("username", quote(user["username"]), samesite="Lax")

    return res


@bp.post("/logout")
def logout():
    session.clear()
    return {"success": True}


@bp.get("/example-authenticated-route")
@require_login
def example_authenticated_route():
    return jsonify("Cool stuff")
