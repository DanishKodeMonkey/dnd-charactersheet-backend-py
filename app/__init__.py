from flask import Flask
from app.routes import register_blueprints
from app.db import disconnect_prisma


def create_app():
    app = Flask(__name__)

    register_blueprints(app)

    @app.teardown_appcontext
    async def shutdown(exception=None):
        await disconnect_prisma()

    return app
