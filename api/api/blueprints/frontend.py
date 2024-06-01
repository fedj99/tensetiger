import os
from glob import glob

from flask import Blueprint, current_app, send_file, send_from_directory

bp = Blueprint("frontend", __name__)


@bp.route("/", defaults={"path": ""})
@bp.route("/<path:path>")
def catch_all(path):
    # Get path in current_app folder
    frontend_path = os.path.realpath(
        os.path.join(os.path.dirname(current_app.root_path), current_app.config["FRONTEND_ROOT"])
    )
    static_path = os.path.realpath(os.path.join(frontend_path, path))

    print("frontend_path", frontend_path)
    print("static_path", static_path)

    def try_path(path):
        candidates = [path, *glob(os.path.join(path, "index.*"))]
        for file in candidates:
            if os.path.exists(file) and os.path.isfile(file):
                # relpath = os.path.relpath(file, frontend_path)
                # return send_from_directory(frontend_path, relpath)
                return send_file(file)
        # Not found
        return None

    # If the path exists and is a file, serve this as a static file
    if res := try_path(static_path):
        return res

    # Otherwise, this is a Vue route, let Vue try to handle it
    return send_from_directory(frontend_path, "index.html")
