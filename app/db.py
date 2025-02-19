import logging
import asyncio
from functools import wraps
from prisma import Prisma, register

logging.basicConfig(level=logging.INFO)

prisma = Prisma()


def prismaQuery(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        logging.info("connecting Prisma")
        await prisma.connect()
        logging.info("prisma connected")
        try:
            result = await func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in query: {e}")
            raise
        finally:
            logging.info("disconnecting Prisma")
            await prisma.disconnect()
            logging.info("prisma disconnected")

        return result

    return wrapper
