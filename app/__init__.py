from flask import Flask
from app.routes import register_blueprints
from app.db import prisma


def create_app():
    app = Flask(__name__)

    register_blueprints(app)

    @app.before_first_request
    async def connect_db():
        await prisma.connect()

    @app.teardown_appcontext
    async def disconnect_db(exception=None):
        await prisma.disconnect()

    return app
