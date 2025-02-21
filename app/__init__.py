from flask import Flask
import asyncio
from app.routes import register_blueprints


def create_app() -> None:

    app = Flask(__name__)

    register_blueprints(app)

    return app
