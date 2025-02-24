from fastapi import APIRouter, HTTPException
from app.db import db

""" Generate API router, will be registered to app in __init__.py """
router = APIRouter()


@router.get("")
async def get_users():
    """Retrieve a list of all users."""
    users = await db.users.find_many()
    return users


@router.post("/create")
async def create_user(user: dict):
    """Create new user with provided data"""
    new_user = await db.users.create(data=user)
    return new_user


@router.get("/{user_id}")
async def get_user(user_id: int):
    """Retrieve a user by ID."""
    user = await db.users.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user  # Return prisma model no conversion
