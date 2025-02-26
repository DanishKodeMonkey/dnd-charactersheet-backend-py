from fastapi import APIRouter, HTTPException, Depends

from app.db import db
from app.schemas.users import UsersLogin
from app.auth import verify_password
from app.utils.auth import create_access_token, verify_access_token


router = APIRouter()


@router.post("/login")
async def login(user: UsersLogin):
    """
    Login endpoint: Authenticate a user based on email and password or OAuth credentials.

    This endpoint allows users to log in either manually (with a password) or using OAuth (Google or Discord).
    It checks whether the user's credentials are valid and, if successful, generates and returns a JWT access token.

    Args:
        user (UsersLogin): The user credentials, which include the email, password (for manual login), and OAuth ID (for OAuth login).

    Raises:
        HTTPException:
            - If the user's email is not found in the database (404).
            - If the password is required but not provided for manual login (400).
            - If the password does not match the stored hash for manual login (400).
            - If OAuth credentials (OAuth ID) are invalid for OAuth login (400).

    Returns:
        dict: A dictionary containing the access token (`access_token`) and the token type (`token_type`, which is always "bearer").
            Example:
            {
                "access_token": "your_jwt_token_here",
                "token_type": "bearer"
            }

    Returned dict is then stored in the user frontend securely, refresh tokens are then generated as needed for consistent access.
    """

    db_user = await db.user.find_unique(where={"email": user.email})

    # Validate user  exists
    if not db_user:
        raise HTTPException(status_code=404, detail="Email not in use")

    # Manual login
    if db_user.oauth_provider == "manual":
        if not user.password:  # Validate password input
            raise HTTPException(
                status_code=400, detail="Password is required for manual account types"
            )
        if not verify_password(
            user.password, db_user.password
        ):  # Verify password with database hash
            raise HTTPException(status_code=400, detail="Invalid password")

    # Oauth login (google or discord)
    elif db_user.oauth_provider in ["google", "discord"]:
        if db_user.oauth_id != user.oauth_id:
            raise HTTPException(status_code=400, detail="Invalid OAuth credentials")

    # Generate JWT token after access authentication
    access_token = create_access_token(data={"sub": str(db_user.id)})

    return {"access_token": access_token, "token_type": "bearer"}
