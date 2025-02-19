from flask import Blueprint, jsonify
from app.db import prismaQuery

users_bp = Blueprint("users", __name__)


# Testing route
@users_bp.route("", methods=["GET"])
@prismaQuery
async def get_users():
    return jsonify({"message": "List of users"})
