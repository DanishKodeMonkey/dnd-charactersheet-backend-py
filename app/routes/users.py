from fastapi import APIRouter, HTTPException
from app.db import db
from app.schemas.users import UserSignUp, UserResponse
from app.services.user_service import create_user, get_user_by_username, get_user_by_id
from app.auth import hash_password

""" Generate API router, will be registered to app in __init__.py """
router = APIRouter()


@router.get("")
async def get_users():
    """
    Remove for production, mainly for testing
    Retrieve a list of all users.

    This endpoint fetches all users from the database. It returns a list of user objects, which includes details like the user's
    name, email, and other profile information.

    Returns:
        List[UserResponse]: A list of user objects represented by the UserResponse Pydantic model.
    """
    users = await db.user.find_many()
    return users


@router.post(
    "/signup", response_model=UserResponse
)  # Response must match pydantic response
async def signup(user: UserSignUp):  # Request must match pydantic UserCreate shape
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
    try:
        new_user = await create_user(user)
        return {"message": "User created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


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
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user  # Return prisma model no conversion
