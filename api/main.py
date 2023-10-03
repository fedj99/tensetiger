import os

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

# Configuration
app.config.from_object("config.default")
app.config.from_object("config.{}".format(os.environ["FLASK_CONFIG"]))

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})


# Main app
@app.get("/")
def index():
    return f"<p>{app.config['APP_NAME']}</p>"
