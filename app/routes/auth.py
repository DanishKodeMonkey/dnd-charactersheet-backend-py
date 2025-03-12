from fastapi import APIRouter, HTTPException
from app.db import db
from app.schemas.users import UserSignIn, UserSignUp
from app.auth import verify_password, hash_password
from app.utils.auth import (
    create_access_token,
    issue_refresh_token,
    verify_refresh_token,
)


router = APIRouter()


@router.post("/signin")
async def signin(user: UserSignIn):
    """
    Login endpoint: Authenticate a user based on email and password or OAuth credentials.

    This endpoint allows users to log in either manually (with a password) or using OAuth (Google or Discord).
    It checks whether the user's credentials are valid and, if successful, generates and returns a JWT access token and refresh token.

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
        as well as a refresh token for increased security and accessability
            Example:
            {
                "access_token": "your_jwt_token_here",
                "token_type": "bearer"
                "refresh_token": "your_refresh_token_here
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
    refresh_token = issue_refresh_token(user_id=str(db_user.id))

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }


@router.post("/refresh")
async def refresh_token(refresh_token: str):
    """
    Refresh endpoint: issue a new access token using a valid refresh.

    This endpoint allows users to refresh their access by providing a valid refresh token
    The refresh token must be valid and not expired, if expired, a new login will be required, and user will be rerouted to login
    If valid, the user will be issued a new access token

    Args:
        refresh_token(str): Refresh token to be validated and used to issue a new token

    Raises:
        HTTPException: If the refresh token is invalid or expired(401)

    Returns:
        dict: A dictionary containing the new access token ('access_token') and the token type ('token_type', always "bearer")
    """
    try:
        user_id = verify_refresh_token(refresh_token)

        # generate access token
        access_token = create_access_token(data={"sub": user_id})

        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as exception:
        # Log error if it occurs, and raise exception to frontend for handling
        return exception
