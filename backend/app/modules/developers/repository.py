import logging

from pymongo.errors import PyMongoError

from app.database import database
from app.modules.developers.schemas import DeveloperSchema, DeveloperUpdateSchema, SocialLinksSchema
from app.modules.theme.schemas import ThemeConfigSchema

logger = logging.getLogger(__name__)

collection = database["developers"]


DEMO_DEVELOPERS: list[DeveloperSchema] = [
    DeveloperSchema(
        id="developer-1",
        name="СК «Атлас девелопмент»",
        slug="atlas",
        logo="",
        phone="+7 (343) 364-56-59",
        email="help@atlas.com",
        website="https://atlas.com",
        socials=SocialLinksSchema(
            vk="https://vk.com/atlas",
            ok="https://ok.ru/atlas",
            telegram="https://t.me/atlas",
        ),
        privacy_policy="",
        domains=["localhost"],
        theme_config=ThemeConfigSchema(
            primaryColor="#1f6feb",
            logo="",
            typography="Inter",
            cardStyle="default",
        ),
    ),
    DeveloperSchema(
        id="developer-2",
        name="ГК «Самолёт»",
        slug="samolet",
        logo="",
        phone="+7 (495) 215-15-15",
        email="info@samolet.ru",
        website="https://samolet.ru",
        socials=SocialLinksSchema(
            vk="https://vk.com/samolet",
            ok="https://ok.ru/samolet",
            telegram="https://t.me/samolet",
        ),
        privacy_policy="",
        domains=["localhost"],
        theme_config=ThemeConfigSchema(
            primaryColor="#e11b4d",
            logo="",
            typography="Jost",
            cardStyle="default",
        ),
    ),
]

DEFAULT_DEVELOPER_SLUG = DEMO_DEVELOPERS[0].slug


def _to_document(developer: DeveloperSchema) -> dict:
    payload = developer.model_dump()
    payload["_id"] = payload.pop("id")

    return payload


def _to_schema(document: dict) -> DeveloperSchema:
    data = {key: value for key, value in document.items() if key != "_id"}
    data["id"] = document["_id"]

    return DeveloperSchema(**data)


async def seed_developers() -> None:
    """Insert demo developers on startup if they are not present yet.

    Uses $setOnInsert so admin edits to existing developers are never
    overwritten on restart.
    """
    try:
        for developer in DEMO_DEVELOPERS:
            await collection.update_one(
                {"_id": developer.id},
                {"$setOnInsert": _to_document(developer)},
                upsert=True,
            )
    except PyMongoError:
        logger.warning("Developer seeding skipped (MongoDB unavailable)")


async def list_developers() -> list[DeveloperSchema]:
    try:
        documents = await collection.find().to_list(length=None)

        if documents:
            return [_to_schema(document) for document in documents]
    except PyMongoError:
        logger.warning("Developers read failed (MongoDB error), using demo defaults")

    return list(DEMO_DEVELOPERS)


async def get_developer(developer_id: str) -> DeveloperSchema | None:
    try:
        document = await collection.find_one({"_id": developer_id})

        if document is not None:
            return _to_schema(document)
    except PyMongoError:
        logger.warning("Developer read failed (MongoDB error), using demo defaults")

    return next((dev for dev in DEMO_DEVELOPERS if dev.id == developer_id), None)


async def get_developer_by_slug(slug: str) -> DeveloperSchema | None:
    try:
        document = await collection.find_one({"slug": slug})

        if document is not None:
            return _to_schema(document)
    except PyMongoError:
        logger.warning("Developer read failed (MongoDB error), using demo defaults")

    return next((dev for dev in DEMO_DEVELOPERS if dev.slug == slug), None)


async def get_developer_by_domain(domain: str) -> DeveloperSchema | None:
    developers = await list_developers()

    match = next((dev for dev in developers if domain in dev.domains), None)

    return match or (developers[0] if developers else None)


async def update_developer(
    developer_id: str,
    payload: DeveloperUpdateSchema,
) -> DeveloperSchema | None:
    existing = await get_developer(developer_id)

    if existing is None:
        return None

    update = payload.model_dump()

    try:
        await collection.update_one({"_id": developer_id}, {"$set": update})
    except PyMongoError:
        logger.warning("Developer update not persisted (MongoDB error)")
        return None

    return await get_developer(developer_id)
