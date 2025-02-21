from flask import Blueprint, jsonify, request
import asyncio
from app.db import prismaQuery
from prisma.models import Users

users_bp = Blueprint("users", __name__)


# Testing route
@users_bp.route("", methods=["GET"])
@prismaQuery
async def get_users():
    try:
        users = await Users.prisma().find_many()
        return {"data": [user.dict() for user in users]}
    except Exception as e:
        return jsonify({"error": f"Failed to get users {str(e)}"}), 500


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
    try:

        user = await Users.prisma().create(data={"email": email, "name": name})
        return jsonify({"message": f"User {name} created successfully"}), 201
    except Exception as e:
        return jsonify({"error": f"Failed to create user: {str(e)}"}), 500
