from fastapi import APIRouter, HTTPException
from app.db import db
from app.schemas.users import UsersLogin
from app.auth import verify_password


router = APIRouter()


@router.post("/login")
async def login(user: UsersLogin):
    """Login endpoint: Check if user is logging in manually or using Oauth"""

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

    return {"message": "Login successful", "user_id": db_user.id}
