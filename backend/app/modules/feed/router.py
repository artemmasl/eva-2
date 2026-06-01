from fastapi import APIRouter

from app.modules.feed.demo_feed import (
    get_feed_buildings,
    get_feed_complexes,
    get_feed_plan_assets,
    get_feed_plan_regions,
    get_feed_spaces,
)
from app.modules.feed.schemas import FeedSyncResultSchema

router = APIRouter(prefix="/api/feed", tags=["feed"])


@router.post("/sync", response_model=FeedSyncResultSchema)
async def sync_feed() -> FeedSyncResultSchema:
    return FeedSyncResultSchema(status="placeholder")


@router.get("/demo")
async def get_demo_feed() -> dict:
    complexes = await get_feed_complexes()
    buildings = await get_feed_buildings()
    spaces = await get_feed_spaces()
    plan_assets = await get_feed_plan_assets()
    plan_regions = await get_feed_plan_regions()

    return {
        "complexes": complexes,
        "buildings": buildings,
        "spaces": spaces,
        "plan_assets": plan_assets,
        "plan_regions": plan_regions,
    }
