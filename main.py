# Entrypoint, app initializer

from app import create_app
from app.db import PrismaInit
import asyncio


def init_app():

    PrismaInit()

    app = create_app()

    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    init_app()
