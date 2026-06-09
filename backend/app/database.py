from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings


client = AsyncIOMotorClient(settings.mongodb_url, serverSelectionTimeoutMS=3000)
database = client[settings.mongodb_database]
