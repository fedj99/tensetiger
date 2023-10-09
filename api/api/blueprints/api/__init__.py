from flask import Blueprint, current_app, jsonify

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
