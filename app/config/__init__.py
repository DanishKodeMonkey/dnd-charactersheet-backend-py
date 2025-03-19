from pydantic_settings import BaseSettings

""" Centralised env variable handling for easy and safe access to variables """


class Settings(BaseSettings):
    JWT_SECRET: str
    DATABASE_URL: str
    ALGORITHM: str = "HS256"  # Default algorithmn HS256
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # default 30
    REFRESH_TOKEN_EXPIRE_HOURS: int = 24  # default 24
    ENVIRONMENT: str = "development"

    class Config:  # Configuration of Settings class
        env_file = ".env"  # env source for Settings class


settings = Settings()  # Instantiate
