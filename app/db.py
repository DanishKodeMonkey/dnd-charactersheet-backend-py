import logging
from prisma import Prisma

logging.basicConfig(level=logging.INFO)
logging.getLogger("prisma").setLevel(logging.DEBUG)

db = Prisma()


async def connect_db():
    """Connect to Prisma database."""
    await db.connect()


async def disconnect_db():
    """Disconenct from the prisma database."""
    await db.disconnect()
