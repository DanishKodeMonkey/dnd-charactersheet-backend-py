from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends, Request, Cookie
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# JWT Expiration config
ACCESS_TOKEN_EXPIRE_MINUTES: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_HOURS: int = settings.REFRESH_TOKEN_EXPIRE_HOURS

# JWT related configuration
SECRET_KEY: str = settings.JWT_SECRET
ALGORITHM: str = settings.ALGORITHM


oauth2_scheme_access = OAuth2PasswordBearer(tokenUrl="signin")


def decode_token(token: str) -> dict:
    """
    Decode a JWT token and return its payload for further processing.
    Raises HTTPException if the token is invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info(f"Decoded token: {payload}")
        return payload
    except JWTError as e:
        logger.warning(f"Token decoding failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def get_refresh_token(request: Request) -> str:
    """
    Extract the refresh token from the cookies in the HTTP request

    """
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing in request")
    return refresh_token


def verify_access_token(access_token: str = Depends(oauth2_scheme_access)) -> str:
    """
    Decode and verify the provided JWT access token.

    Args:
        token (str): The JWT token to be verified, typically provided in the Authorization header.

    Returns:
        str: The user ID extracted from the payload of the token if valid.

    Raises:
        HTTPException: If the token is invalid or cannot be decoded, an exception is raised with a 401 status code.
    """
    payload = decode_token(access_token)
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid access token type")
    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="invalid token")
    return user_id


def verify_refresh_token(refresh_token: str = Depends(get_refresh_token)) -> str:
    """
    Verifies provided refresh token and extracts the user ID from it

    Args:
        refresh_token(str): The refresh token to be verified

    Returns:
        str: The user ID to be extracted from the refresh token's payload

    Raises:
        HTTPException: If the refresh token is invalid or expired, an exception is raised
    """
    payload = decode_token(refresh_token)

    if payload.get("type") != "refresh_token":
        raise HTTPException(status_code=401, detail="Invalid refresh token type")
    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    if datetime.now(timezone.utc) > datetime.fromtimestamp(payload["exp"]):
        raise HTTPException(status_code=401, detail="Refresh token has expired")

    return user_id


def verify_session(
    refresh_token: str = Depends(get_refresh_token),
    access_token: str = Depends(oauth2_scheme_access),
):
    """
    Verify both access token and refresh token

    Will be used for endpoint verify to check validity of both access and refresh tokens.
    Returns success if both tokens are valid
    If either token is invalid, raises a 401, unauthorized.

    Args:
        refresh_token(str): The refresh token provided in the request body
        access_token(str): The access token extracted from Authorization header

    Returns:
        bool: Access tokens match

    Raises:
        HTTPException: If either token is invalid or expired, returns a 401 status code.
    """
    try:
        access_user_id = verify_access_token(access_token)
        refresh_user_id = verify_refresh_token(refresh_token)
        logger.info(access_user_id)
        logger.info(refresh_user_id)

        # Check if both tokens belong to the same user
        if access_user_id != refresh_user_id:
            raise HTTPException(status_code=401, detail="Tokens do not match")

        return access_user_id
    except JWTError as e:
        raise HTTPException(
            status_code=401, detail=f"Invalid or expired token: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


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
    to_encode.update({"exp": expire, "type": "access"})
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
    payload = {"sub": user_id, "exp": expire, "type": "refresh"}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
