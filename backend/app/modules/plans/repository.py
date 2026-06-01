from app.modules.feed.demo_feed import get_feed_plan_assets, get_feed_plan_regions
from app.modules.plans.schemas import PlanAssetSchema, PlanKind, PlanRegionSchema


def map_feed_asset_to_schema(feed_asset: dict) -> PlanAssetSchema:
    return PlanAssetSchema(
        id=feed_asset["id"],
        complex_id=feed_asset["complex_id"],
        kind=feed_asset["kind"],
        target_id=feed_asset["target_id"],
        image_url=feed_asset["image_url"],
        width=feed_asset["width"],
        height=feed_asset["height"],
    )


def map_feed_region_to_schema(feed_region: dict) -> PlanRegionSchema:
    return PlanRegionSchema(
        id=feed_region["id"],
        asset_id=feed_region["asset_id"],
        points=feed_region["points"],
        target_kind=feed_region["target_kind"],
        target_id=feed_region["target_id"],
        label=feed_region["label"],
        status=feed_region["status"],
    )


async def get_plan_assets(
    complex_id: str | None = None,
    kind: PlanKind | None = None,
    target_id: str | None = None,
) -> list[PlanAssetSchema]:
    feed_assets = await get_feed_plan_assets()
    assets = [map_feed_asset_to_schema(feed_asset) for feed_asset in feed_assets]

    return [
        asset
        for asset in assets
        if (complex_id is None or asset.complex_id == complex_id)
        and (kind is None or asset.kind == kind)
        and (target_id is None or asset.target_id == target_id)
    ]


async def get_plan_asset(asset_id: str) -> PlanAssetSchema | None:
    assets = await get_plan_assets()

    return next((asset for asset in assets if asset.id == asset_id), None)


async def get_plan_regions(asset_id: str) -> list[PlanRegionSchema]:
    feed_regions = await get_feed_plan_regions()

    return [
        map_feed_region_to_schema(feed_region)
        for feed_region in feed_regions
        if feed_region["asset_id"] == asset_id
    ]
