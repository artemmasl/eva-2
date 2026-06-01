from app.modules.buildings.schemas import BuildingSchema, CoordinatesSchema
from app.modules.feed.demo_feed import get_feed_buildings


def map_feed_building_to_schema(feed_building: dict) -> BuildingSchema:
    coordinates = feed_building["coordinates"]

    return BuildingSchema(
        id=feed_building["id"],
        complex_id=feed_building["complex_id"],
        developer_id=feed_building["developer_id"],
        name=feed_building["name"],
        address=feed_building["address"],
        coordinates=CoordinatesSchema(
            lat=coordinates["lat"],
            lng=coordinates["lng"],
        ),
    )


async def get_buildings() -> list[BuildingSchema]:
    feed_buildings = await get_feed_buildings()

    return [map_feed_building_to_schema(feed_building) for feed_building in feed_buildings]
