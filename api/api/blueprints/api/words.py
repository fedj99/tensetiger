from flask import Blueprint, current_app, jsonify

from api import db

bp = Blueprint("words", __name__)


@bp.get("/words")
def get_all_words():
    return jsonify(db.get_all(db.T_WORDS))


@bp.get("/words/batch")
def get_word_batch():
    game_config = current_app.config["GAME_CONFIG"]
    return jsonify(db.get_random_subset(db.T_WORDS, game_config["wordCount"]))
