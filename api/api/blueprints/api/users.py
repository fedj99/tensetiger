from flask import Blueprint, jsonify

from api import db

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.get("/<int:id>")
def get_user(id: int):  # pylint: disable=redefined-builtin
    return jsonify(db.find_by_id(db.T_USERS, id))
