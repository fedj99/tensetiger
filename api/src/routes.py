import os
from datetime import datetime
from time import time

from flask import Flask, jsonify, make_response, request, session

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
        response.set_cookie("username", user["username"], samesite="lax")
        response.set_cookie("user_id", str(user["id"]), samesite="lax")
        return response

    @app.get("/api/")
    def index():
        return f"<p>{app.config['APP_NAME']}</p>"

    @app.get("/api/scores")
    def scores():
        return db.get_all(db.T_SCORES)

    @app.post("/api/scores")
    def add_score():
        success = db.create(db.T_SCORES, request.json) > 0
        response = make_response({"success": success})
        response.status_code = 201 if success else 400
        return response

    @app.get("/api/words")
    def get_all_words():
        if "count" in request.args:
            count = int(request.args["count"])
            return db.get_random_subset(db.T_WORDS, count)
        else:
            return db.get_all(db.T_WORDS)

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def catch_all(path):
        # Get path in app folder
        static_path = os.path.join(app.static_folder, path)
        # If the path exists and is a file, serve this as a static file
        if os.path.exists(static_path) and os.path.isfile(static_path):
            return app.send_static_file(path)
        # Otherwise, this is a Vue route, let Vue handle it
        return app.send_static_file("index.html")
