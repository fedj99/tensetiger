import os

from dotenv import load_dotenv


def setup_env():
    # Environment
    load_dotenv()
    load_dotenv(".env.local")

    if "FLASK_CONFIG" not in os.environ:
        raise KeyError("`FLASK_CONFIG` not defined in environment")

    config_mode = os.environ["FLASK_CONFIG"]
    load_dotenv(f".env.{config_mode}")
    load_dotenv(f".env.{config_mode}.local")

    return config_mode
