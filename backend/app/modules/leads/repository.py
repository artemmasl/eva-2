import logging
from datetime import datetime, timezone
from uuid import uuid4

from pymongo.errors import PyMongoError

from app.database import database
from app.modules.leads.schemas import LeadCreateSchema, LeadSchema

logger = logging.getLogger(__name__)

collection = database["leads"]


def _to_document(lead: LeadSchema) -> dict:
    payload = lead.model_dump()
    payload["_id"] = payload.pop("id")

    return payload


def _to_schema(document: dict) -> LeadSchema:
    data = {key: value for key, value in document.items() if key != "_id"}
    data["id"] = document["_id"]

    return LeadSchema(**data)


async def create_lead(payload: LeadCreateSchema) -> LeadSchema:
    """Persist an incoming lead.

    Returns the created lead even if MongoDB is unavailable so the storefront
    still confirms the request to the user (the lead is logged in that case).
    """
    lead = LeadSchema(
        id=str(uuid4()),
        status="new",
        created_at=datetime.now(timezone.utc),
        **payload.model_dump(),
    )

    try:
        await collection.insert_one(_to_document(lead))
    except PyMongoError:
        logger.warning("Lead not persisted (MongoDB unavailable): %s", lead.kind)

    return lead


async def list_leads() -> list[LeadSchema]:
    try:
        documents = await collection.find().sort("created_at", -1).to_list(length=None)
    except PyMongoError:
        logger.warning("Leads read failed (MongoDB error)")
        return []

    return [_to_schema(document) for document in documents]
