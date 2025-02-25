from pydantic import BaseModel, EmailStr, Field

# Input validation
class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=4, max_length=30,regex="^[a-zA-Z ]+$") # Regex limited to letters & spaces

# Output validation (responses)
class UserResponse(BaseModel)
    id: int
    email: EmailStr
    name: str

    class Config:
        from_attributes = True