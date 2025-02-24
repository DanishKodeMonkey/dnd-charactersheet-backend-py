import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from app.db import connect_db, disconnect_db
from app.routes import register_routers


def create_app() -> FastAPI:

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Load database using prisma
        await connect_db()
        yield
        # Disconnect prisma after use
        await disconnect_db()

    app = FastAPI(title="FastApi Prisma dnd API", lifespan=lifespan)
    register_routers(app)

    return app
