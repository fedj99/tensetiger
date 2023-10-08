import json
import os
from datetime import datetime
from glob import glob
from time import sleep
from urllib.parse import quote

from flask import Flask, jsonify, redirect, request, send_file, send_from_directory

import db


def setup_routes(app: Flask):
    @app.get("/ping")
    def ping():
        return jsonify("pong")

    @app.post("/api/login")
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

    @app.get("/api/")
    def index():
        return jsonify(app.config["APP_NAME"])

    @app.get("/api/users/<int:id>")
    def get_user(id: int):
        return jsonify(db.find_by_id(db.T_USERS, id))

    @app.get("/api/scores")
    def scores():
        return jsonify(db.get_all(db.T_SCORES))

    @app.post("/api/scores")
    def post_score():
        score_id = db.create(db.T_SCORES, request.json)
        response = jsonify({"score_id": score_id})
        return response

    @app.get("/api/scores/topk")
    def get_top_k_scores():
        k = int(request.args.get("k", 5))
        return jsonify(db.get_top_k(db.T_SCORES, "score", k))

    @app.get("/api/scores/latest")
    def get_latest_scores():
        user_id = int(request.args.get("user_id", -1))
        k = int(request.args.get("k", 5))
        return jsonify(db.get_top_k_filtered(db.T_SCORES, "date", "user_id", user_id, k))

    @app.get("/api/scores/highscore")
    def get_highscore():
        user_id = int(request.args.get("user_id", -1))
        return jsonify(db.get_max(db.T_SCORES, "score", "user_id", user_id))

    @app.get("/api/scores/<int:id>")
    def get_score(id: int):
        return jsonify(db.find_by_id(db.T_SCORES, id))

    @app.get("/api/words")
    def get_all_words():
        return jsonify(db.get_all(db.T_WORDS))

    @app.get("/api/words/batch")
    def get_word_batch():
        game_config = app.config["GAME_CONFIG"]
        return jsonify(db.get_random_subset(db.T_WORDS, game_config["wordCount"]))

    @app.get("/api/game-config")
    def game_config():
        return app.config["GAME_CONFIG"]

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def catch_all(path):
        # Get path in app folder
        frontend_path = app.config["FRONTEND_ROOT"]
        static_path = os.path.join(frontend_path, path)

        def try_path(path):
            candidates = [path, *glob(os.path.join(path, "index.*"))]
            for file in candidates:
                app.logger.debug(f"Trying: `{file}`")
                if os.path.exists(file) and os.path.isfile(file):
                    # relpath = os.path.relpath(file, frontend_path)
                    # return send_from_directory(frontend_path, relpath)
                    return send_file(file)

        # If the path exists and is a file, serve this as a static file
        if res := try_path(static_path):
            return res

        # Otherwise, this is a Vue route, let Vue try to handle it
        return send_from_directory(frontend_path, "index.html")

    def jsonify_exc(e: Exception):
        return jsonify({"error": e.__class__.__name__, "message": str(e)})

    @app.errorhandler(404)
    def not_found(e: Exception):
        if request.is_json:
            return jsonify_exc(e), 404
        return redirect("/not-found")

    @app.errorhandler(400)
    def bad_request(e):
        if request.is_json:
            return jsonify_exc(e), 400
        return redirect("/bad-request")

    @app.errorhandler(500)
    def internal_server_error(e):
        if request.is_json:
            return jsonify_exc(e), 500
        return redirect("/internal-server-error")
