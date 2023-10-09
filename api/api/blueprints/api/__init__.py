from flask import Blueprint, current_app, g, jsonify, session

from api import db

from . import auth, game, scores, users, words

bp = Blueprint("api", __name__, url_prefix="/api")

bp.register_blueprint(auth.bp)
bp.register_blueprint(users.bp)
bp.register_blueprint(scores.bp)
bp.register_blueprint(words.bp)
bp.register_blueprint(game.bp)


@bp.get("/")
def get_index():
    return jsonify(current_app.config["APP_NAME"])


@bp.before_request
def load_user():
    if "user_id" in session:
        user = db.find_by_id(db.T_USERS, session["user_id"])
        g.user = user
    else:
        g.user = None
