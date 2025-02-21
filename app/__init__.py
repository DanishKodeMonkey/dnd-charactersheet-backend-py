from flask import Flask
from app.routes import register_blueprints
from app.db import disconnect_prisma
import asyncio


def create_app() -> None:
    app = Flask(__name__)

    register_blueprints(app)

    return app
