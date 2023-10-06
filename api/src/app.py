import os

import rich.traceback
from flask import Flask
from flask_cors import CORS

import config
import db
import env
import routes

rich.traceback.install()


def create_app():
    config_mode = env.setup_env()

    # Create app
    root_path = os.path.dirname(os.path.dirname(__file__))  # Go up one directory
    app = Flask(__name__, root_path=root_path)
    app.logger.debug(f"Root path: {root_path}")

    # Configuration
    config.setup_config(app, config_mode)

    # Set secret key for session cookies
    app.secret_key = app.config["COOKIES_SK"]

    # Enable CORS
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # Register database commands and teardown command
    db.init_app(app)

    # Register all routes
    routes.setup_routes(app)

    return app
