from flask import Blueprint, current_app

bp = Blueprint("game", __name__)


@bp.get("/game-config")
def game_config():
    return current_app.config["GAME_CONFIG"]
