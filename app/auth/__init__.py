import bcrypt


def hash_password(password: str) -> str:
    """Hashes password"""
    salt = bcrypt.gensalt()  # Generate salt
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")  # Return hashed password as a string


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )
