import os

import rich.traceback
from flask import Flask, make_response, request
from flask_cors import CORS

from db import DB, T_SCORES, T_WORDS

rich.traceback.install()

app = Flask(__name__)

# Configuration
app.config.from_object("config.default")
app.config.from_object("config.{}".format(os.environ["FLASK_CONFIG"]))
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
