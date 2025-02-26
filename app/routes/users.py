from fastapi import APIRouter, HTTPException
from app.db import db
from app.schemas.users import UserCreate, UserResponse
from app.auth import hash_password

""" Generate API router, will be registered to app in __init__.py """
router = APIRouter()


@router.get("")
async def get_users():
    """
    Retrieve a list of all users.

    This endpoint fetches all users from the database. It returns a list of user objects, which includes details like the user's
    name, email, and other profile information.

    Returns:
        List[UserResponse]: A list of user objects represented by the UserResponse Pydantic model.
    """
    users = await db.user.find_many()
    return users


@router.post(
    "/create", response_model=UserResponse
)  # Response must match pydantic response
async def create_user(user: UserCreate):  # Request must match pydantic UserCreate shape
    """
    Create a new user with the provided data.

    This endpoint validates the input data (ensuring no duplicate email exists) and, if valid, creates a new user in the database.
    The password is hashed before being saved.

    Args:
        user (UserCreate): The user creation data, including name, email, and password, validated by the UserCreate Pydantic model.

    Raises:
        HTTPException: If the email is already in use, a 400 status code with a detail message will be returned.

    Returns:
        UserResponse: The created user's data, represented by the UserResponse Pydantic model.
    """
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

    new_user = await db.user.create(data=user_data)
    return new_user


@router.get("/{user_id}")
async def get_user(user_id: int):
    """
    Retrieve a user by their ID.

    This endpoint fetches the details of a single user by their unique ID. If no user is found with the given ID, a 404 error is raised.

    Args:
        user_id (int): The ID of the user to be retrieved.

    Raises:
        HTTPException: If no user is found with the given ID, a 404 status code with a detail message will be returned.

    Returns:
        UserResponse: The user's data, represented by the UserResponse Pydantic model.
    """
    user = await db.user.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user  # Return prisma model no conversion
