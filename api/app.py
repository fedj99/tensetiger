import os

import rich.traceback
from dotenv import load_dotenv
from flask import Flask, make_response, request
from flask_cors import CORS

from db import DB, T_SCORES, T_WORDS

rich.traceback.install()


def create_app():
    # Environment
    load_dotenv()
    load_dotenv(".env.local")

    if "FLASK_CONFIG" not in os.environ:
        raise KeyError("`FLASK_CONFIG` not defined in environment")

    config_mode = os.environ["FLASK_CONFIG"]
    load_dotenv(f".env.{config_mode}")
    load_dotenv(f".env.{config_mode}.local")

    # Create app
    app = Flask(__name__)

    # Load configuration
    app.config.from_object("config.default")
    app.config.from_object(f"config.{config_mode}")
    app.config.from_prefixed_env()  # Load all FLASK_* variables

    # Enable CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    # TODO: Clean up database code with proper tear-down
    db = DB(app)
    db.connect()

    # Main app
    @app.get("/api/")
    def index():
        return f"<p>{app.config['APP_NAME']}</p>"

    @app.get("/api/scores")
    def scores():
        return db.get_all(T_SCORES)

    @app.post("/api/scores")
    def add_score():
        success = db.create(T_SCORES, request.json) > 0
        response = make_response({"success": success})
        response.status_code = 201 if success else 400
        return response

    @app.get("/api/words")
    def get_all_words():
        if "count" in request.args:
            count = int(request.args["count"])
            return db.get_random_subset(T_WORDS, count)
        else:
            return db.get_all(T_WORDS)

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

    return app
