import logging
import asyncio
from functools import wraps
from prisma import Prisma, register

logging.basicConfig(level=logging.INFO)


def PrismaInit():
    logging.info("Initiating Prisma...")
    prisma = Prisma()
    logging.info("Prisma Initiated")
    logging.info("Connecting prisma to Database")
    prisma.connect()
    logging.info("Prisma connected to database")
    logging.info("Registering Prisma client...")
    register(prisma)  # Register operation lifecycle with prisma
    logging.info("Prisma client registered")


""" 
Below deprecated for now, turns out continous 
connection/disconnections is expensive and is better to generally just let Prisma handle it 
"""

""" async def connect_prisma():
    logging.info("connecting Prisma")
    await prisma.connect()
    logging.info("prisma connected")


async def disconnect_prisma():
    logging.info("disconnecting Prisma")
    await prisma.disconnect()
    logging.info("prisma disconnected")


def prismaQuery(func):
    Decorator ensures Prisma is connected before executing the query

    @wraps(func)
    async def wrapper(*args, **kwargs):
        if not prisma.is_connected():
            await connect_prisma()
        try:
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            logging.error(f"Error in query: {e}")
            raise

    return wrapper
 """
