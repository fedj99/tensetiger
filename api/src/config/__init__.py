import os

from flask import Flask, current_app

_app: Flask = None


def setup_config(app: Flask, config_mode: str):
    # Set global app variable for config functions to use
    global _app
    _app = app

    # Load configuration
    app.config.from_object("config.default")
    app.config.from_object(f"config.{config_mode}")
    app.config.from_prefixed_env()  # Load all FLASK_* variables


def add_prefix(path: str):
    global _app
    with _app.app_context():
        return os.path.join(current_app.root_path, path)
