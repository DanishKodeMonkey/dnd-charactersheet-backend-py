from flask import Blueprint, jsonify

characters_bp = Blueprint("characters", __name__)


# Testing route
@characters_bp.route("", methods=["GET"])
def get_characters():
    return jsonify({"message": "List of characters"})
