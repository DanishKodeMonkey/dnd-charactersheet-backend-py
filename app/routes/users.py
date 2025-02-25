from fastapi import APIRouter, HTTPException
from app.db import db
from app.schemas.users import UserCreate, UserResponse
from app.auth import hash_password

""" Generate API router, will be registered to app in __init__.py """
router = APIRouter()


@router.get("")
async def get_users():
    """Retrieve a list of all users."""
    users = await db.user.find_many()
    return users


@router.post(
    "/create", response_model=UserResponse
)  # Response must match pydantic response
async def create_user(user: UserCreate):  # Request must match pydantic UserCreate shape
    """API-level validation, if failed will not reach prisma, saves DB calls"""
    existing = await db.user.find_unique({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already in use")
    if user.password:
        hashed_password = hash_password(user.password)
    else:
        hashed_password = None

    user_data = user.model_dump()
    if hashed_password:
        user_data["password"] = hashed_password

    """Create new user with provided data"""
    new_user = await db.user.create(data=user_data)
    return new_user


@router.get("/{user_id}")
async def get_user(user_id: int):
    """Retrieve a user by ID."""
    user = await db.user.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user  # Return prisma model no conversion
