from flask import Blueprint, jsonify, request
from app.db import prismaQuery
from prisma.models import User

users_bp = Blueprint("users", __name__)


# Testing route
@users_bp.route("", methods=["GET"])
@prismaQuery
async def get_users():
    return jsonify({"message": "List of users"})


@users_bp.route("/create", methods=["POST"])
@prismaQuery
async def create_user():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Invalid data provided"})

    name = data.get("name")
    email = data.get("email")

    if name is None or email is None:
        return jsonify({"error": "You need to provide a name and a email"})

    user = await User.prisma().create(data={"email": email, "name": name})

    return jsonify(user), 201
