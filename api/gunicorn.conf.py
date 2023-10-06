"""
gUnicorn server settings
"""

import os

_host = os.environ.get("GUNICORN_SERVER_HOST") or "0.0.0.0"
_port = os.environ.get("GUNICORN_SERVER_PORT") or "8000"

# Main settings
bind = f"{_host}:{_port}"
wsgi_app = "run:app"
