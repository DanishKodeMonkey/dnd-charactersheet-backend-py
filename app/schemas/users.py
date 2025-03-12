from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


# Input validation
class UserSignUp(BaseModel):  # Extend pydantic basemodel for validation
    email: EmailStr
    username: str = Field(
        ..., min_length=4, max_length=30, pattern="^[a-zA-Z0-9_]+$"
    )  # Regex limited to letters, spaces and underscores
    password: Optional[str]  # Optional for Oauth users
    oauth_provider: Optional[str] = "manual"  # oAuth provider (google, discord, manual)
    oauth_id: Optional[str] = None  # Optional oAuth ID

    class Config:
        # Ensure values can be passed through ORM PRisma client
        orm_mode: True


# Output validation (responses)
class UserResponse(BaseModel):
    id: UUID  # Accomidate UUID type
    username: str
    email: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Map prisma model attributes to pydantic fields


class UserSignIn(BaseModel):
    email: EmailStr
    password: str | None = None
    oauth_id: str | None = None
