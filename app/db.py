import logging
import asyncio
from functools import wraps
from prisma import Prisma, register

logging.basicConfig(level=logging.INFO)

prisma = Prisma()


def prismaQuery(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        await prisma.connect()

        try:
            result = await func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in query: {e}")
            raise
        finally:
            await prisma.disconnect()

        return result

    return wrapper
