from flask import Blueprint, jsonify

users_bp = Blueprint("users", __name__)


# Testing route
@users_bp.route("/", methods=["GET"])
def get_users():
    return jsonify({"message": "List of users"})
