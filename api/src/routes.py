import os

from flask import Flask, make_response, request

import db


def setup_routes(app: Flask):
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
