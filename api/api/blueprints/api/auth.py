from datetime import datetime
from urllib.parse import quote

from flask import Blueprint, jsonify, request

from api import db

bp = Blueprint("auth", __name__)


@bp.post("/login")
def login():
    username = request.json["username"]
    user = db.find_by(db.T_USERS, "username", username, single=True)
    if user:
        # Update last login time
        db.update(db.T_USERS, user["id"], {"last_logon": datetime.now().isoformat()})
    else:
        # Create user
        user_id = db.create(db.T_USERS, {"username": username})
        user = db.find_by_id(db.T_USERS, user_id)

    response = jsonify({"success": True, "user": user})
    # session["sess_username"] = user["username"]
    # session["sess_user_id"] = user["id"]
    response.set_cookie("username", quote(user["username"]), samesite="lax")
    response.set_cookie("user_id", quote(str(user["id"])), samesite="lax")
    return response
