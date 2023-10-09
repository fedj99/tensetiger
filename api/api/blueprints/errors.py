from flask import Blueprint, jsonify, redirect, request

bp = Blueprint("errors", __name__)


def jsonify_exc(e: Exception):
    return jsonify({"error": e.__class__.__name__, "message": str(e)})


@bp.errorhandler(404)
def not_found(e: Exception):
    if request.is_json:
        return jsonify_exc(e), 404
    return redirect("/not-found")


@bp.errorhandler(400)
def bad_request(e):
    if request.is_json:
        return jsonify_exc(e), 400
    return redirect("/bad-request")


@bp.errorhandler(500)
def internal_server_error(e):
    if request.is_json:
        return jsonify_exc(e), 500
    return redirect("/internal-server-error")
