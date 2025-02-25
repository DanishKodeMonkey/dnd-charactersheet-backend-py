from fastapi import APIRouter, HTTPException, Depends
from app.db import db
from app.schemas.users import UserCreate, UserResponse
from prisma.models import Users

""" Generate API router, will be registered to app in __init__.py """
router = APIRouter()


@router.get("")
async def get_users():
    """Retrieve a list of all users."""
    users = await db.users.find_many()
    return users


@router.post(
    "/create", response_model=UserResponse
)  # Response must match pydantic response
async def create_user(user: UserCreate):  # Request must match pydantic UserCreate shape
    """API-level validation, if failed will not reach prisma, saves DB calls"""
    existing = db.users.find_unique({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already in use")

    """Create new user with provided data"""
    new_user = await db.users.create(data=user.model_dump())
    return new_user


@router.get("/{user_id}")
async def get_user(user_id: int):
    """Retrieve a user by ID."""
    user = await db.users.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user  # Return prisma model no conversion
