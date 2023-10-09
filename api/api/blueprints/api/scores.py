from flask import Blueprint, jsonify, request

from api import db
from api.blueprints.api.auth import require_login

bp = Blueprint("scores", __name__)


@bp.get("/scores")
def scores():
    return jsonify(db.get_all(db.T_SCORES))


@bp.post("/scores")
@require_login
def post_score():
    score_id = db.create(db.T_SCORES, request.json)
    response = jsonify({"score_id": score_id})
    return response


@bp.get("/scores/topk")
def get_top_k_scores():
    k = int(request.args.get("k", 5))
    return jsonify(db.get_top_k(db.T_SCORES, "score", k))


@bp.get("/scores/latest")
def get_latest_scores():
    user_id = int(request.args.get("user_id", -1))
    k = int(request.args.get("k", 5))
    return jsonify(db.get_top_k_filtered(db.T_SCORES, "date", "user_id", user_id, k))


@bp.get("/scores/highscore")
def get_highscore():
    user_id = int(request.args.get("user_id", -1))
    return jsonify(db.get_max(db.T_SCORES, "score", "user_id", user_id))


@bp.get("/scores/<int:id>")
def get_score(id: int):  # pylint: disable=redefined-builtin
    return jsonify(db.find_by_id(db.T_SCORES, id))
