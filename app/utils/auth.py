from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.config import settings

# JWT Expiration config
ACCESS_TOKEN_EXPIRE_MINUTES: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_HOURS: int = settings.REFRESH_TOKEN_EXPIRE_HOURS

# JWT related configuration
SECRET_KEY: str = settings.JWT_SECRET
ALGORITHM: str = settings.ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_access_token(token: str = Depends(oauth2_scheme)) -> str:
    """
    Decode and verify the provided JWT access token.

    Args:
        token (str): The JWT token to be verified, typically provided in the Authorization header.

    Returns:
        str: The user ID extracted from the payload of the token if valid.

    Raises:
        HTTPException: If the token is invalid or cannot be decoded, an exception is raised with a 401 status code.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Generate a JWT access token for the given data.

    Args:
        data (dict): The data to be encoded into the JWT payload. Typically includes user information.
        expires_delta (timedelta, optional): The expiration duration for the token. If None, defaults to
                                              the value from settings.

    Returns:
        str: The generated JWT access token as a string.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(user_id: str) -> str:
    """
    Generate a JWT refresh token with a 24-hour expiration for the given user ID.

    Args:
        user_id (str): The user ID to be encoded into the payload of the refresh token.

    Returns:
        str: The generated JWT refresh token as a string.
    """
    expire = datetime.now(timezone.utc) + timedelta(hours=REFRESH_TOKEN_EXPIRE_HOURS)
    payload = {"sub": user_id, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_refresh_token(refresh_token: str) -> str:
    """
    Verifies provided refresh token and extracts the user ID from it

    Args:
        refresh_token(str): The refresh token to be verified

    Returns:
        str: The user ID to be extracted from the refresh token's payload

    Raises:
        HTTPException: If the refresh token is invalid or expired, an exception is raised
    """
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token. Please log in again.",
        )
