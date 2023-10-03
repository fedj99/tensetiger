import os

import rich.traceback
from db import DB
from flask import Flask
from flask_cors import CORS

rich.traceback.install()

app = Flask(__name__)

# Configuration
app.config.from_object("config.default")
app.config.from_object("config.{}".format(os.environ["FLASK_CONFIG"]))
app.config.from_prefixed_env()  # Load all FLASK_* variables

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})

db = DB()


# Main app
@app.get("/api/")
def index():
    return f"<p>{app.config['APP_NAME']}</p>"


@app.get("/api/scores")
def scores():
    return db.get_all("scores")
