from fastapi import FastAPI
from .users import router as users_router
from .characters import router as characters_router
from .auth import router as auth_router


def register_routers(app: FastAPI) -> None:
    app.include_router(users_router, prefix="/users", tags=["Users"])
    app.include_router(characters_router, prefix="/characters", tags=["Characters"])
    app.include_router(auth_router, prefix="/auth", tags=["Auth"])
