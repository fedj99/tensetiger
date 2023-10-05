from flask import Flask


def setup_config(app: Flask, config_mode: str):
    # Load configuration
    app.config.from_object("config.default")
    app.config.from_object(f"config.{config_mode}")
    app.config.from_prefixed_env()  # Load all FLASK_* variables
