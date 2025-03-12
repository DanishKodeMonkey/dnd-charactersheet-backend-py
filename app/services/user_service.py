from fastapi import HTTPException, status
from app.db import db
from app.auth import hash_password, verify_password
from app.schemas.users import UserSignUp, UserSignIn

""" HUSKAT accept Oauth providers for google and discord """


async def create_user(user_signup: UserSignUp):
    existing_user = await db.user.find_unique(where={"email": user_signup.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use"
        )

    hashed_password = hash_password(user_signup.password)
    user_data = user_signup.model_dump()
    user_data["password"] = hashed_password

    try:
        new_user = await db.user.create(data=user_data)
        return new_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occured while creating the user: {str(e)}",
        )


async def get_user_by_username(username: str):
    user = await db.user.find_unique(where={"username": username})
    return user


async def get_user_by_id(user_id: int):
    """Fetch user by ID"""
    user = await db.user.find_unique(where={"id": user_id})
    if not user:
        raise ValueError("User not found")
    return user


""" HUSKAT update user method """
