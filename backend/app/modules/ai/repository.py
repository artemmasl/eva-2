import logging
from datetime import datetime, timezone

from pymongo.errors import PyMongoError

from app.database import database

logger = logging.getLogger(__name__)

collection = database["ai_conversations"]

MAX_STORED_MESSAGES = 40


async def get_history(session_id: str) -> list[dict]:
    try:
        document = await collection.find_one({"_id": session_id})
    except PyMongoError:
        logger.warning("AI history unavailable (MongoDB error), continuing without history")
        return []

    if document is None:
        return []

    return document.get("messages", [])


async def append_message(session_id: str, role: str, content: str) -> None:
    message = {
        "role": role,
        "content": content,
        "created_at": datetime.now(timezone.utc),
    }

    try:
        await collection.update_one(
            {"_id": session_id},
            {
                "$push": {"messages": {"$each": [message], "$slice": -MAX_STORED_MESSAGES}},
                "$set": {"updated_at": message["created_at"]},
            },
            upsert=True,
        )
    except PyMongoError:
        logger.warning("AI history not saved (MongoDB error)")


async def clear_history(session_id: str) -> None:
    try:
        await collection.delete_one({"_id": session_id})
    except PyMongoError:
        logger.warning("AI history not cleared (MongoDB error)")
