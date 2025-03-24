import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.db import connect_db, disconnect_db
from app.routes import register_routers


def create_app() -> FastAPI:

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Load database using prisma
        await connect_db()
        yield  # Pause here until application is shut down
        # Disconnect prisma after use
        await disconnect_db()

    app = FastAPI(title="FastApi Prisma dnd API", lifespan=lifespan)

    origins = ["http://localhost:5173"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_routers(app)

    return app
