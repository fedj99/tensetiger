import os

import rich.traceback
from flask import Flask
from flask_cors import CORS

from api import blueprints, db

rich.traceback.install()

from dotenv import load_dotenv


def setup_env():
    # Environment
    load_dotenv()
    load_dotenv(".env.local")

    if "FLASK_ENV" not in os.environ:
        raise KeyError("`FLASK_ENV` not defined in environment")

    config_mode = os.environ["FLASK_ENV"]
    load_dotenv(f".env.{config_mode}")
    load_dotenv(f".env.{config_mode}.local")

    return config_mode


def create_app():
    config_mode = setup_env()

    # Create app
    app = Flask(__name__)

    app.logger.info("Running application in %s mode", config_mode)

    # Configuration
    app.config.from_object("api.config.default")
    app.config.from_object(f"api.config.{config_mode}")
    app.config.from_prefixed_env()

    # Enable CORS in dev mode. In prod mode, api should be hosted under same domain
    if os.environ["FLASK_ENV"] == "development":
        CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # Register database commands and teardown command
    db.init_app(app)

    # Register all routes
    app.register_blueprint(blueprints.api.bp)
    app.register_blueprint(blueprints.misc.bp)
    app.register_blueprint(blueprints.frontend.bp)
    app.register_blueprint(blueprints.errors.bp)

    app.logger.info("Server started successfully")

    return app
