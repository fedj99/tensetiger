from flask import Blueprint, jsonify


bp = Blueprint("misc", __name__)


@bp.get("/ping")
def get_ping():
    return jsonify("pong")
