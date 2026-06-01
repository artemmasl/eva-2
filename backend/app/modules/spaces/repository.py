from app.modules.feed.demo_feed import get_feed_buildings, get_feed_complexes, get_feed_spaces
from app.modules.spaces.schemas import NumberRangeSchema, PriceSchema, SpaceFiltersMetaSchema, SpaceSchema


def map_feed_space_to_schema(
    feed_space: dict,
    buildings_by_id: dict[str, dict],
    complexes_by_id: dict[str, dict],
) -> SpaceSchema:
    price = feed_space["price"]
    building = buildings_by_id.get(feed_space["building_id"], {})
    complex = complexes_by_id.get(building.get("complex_id", ""), {})

    return SpaceSchema(
        id=feed_space["id"],
        complex_id=building.get("complex_id", ""),
        complex_name=complex.get("name", ""),
        building_id=feed_space["building_id"],
        building_name=building.get("name", feed_space["building_id"]),
        building_address=building.get("address", ""),
        building_district=building.get("district", ""),
        building_metro=building.get("metro", ""),
        building_metro_time=building.get("metro_time", ""),
        stype=feed_space["stype"],
        is_apartment=feed_space["is_apartment"],
        rooms=feed_space["rooms"],
        area=feed_space["area"],
        floor=feed_space["floor"],
        floors_total=feed_space["floors_total"],
        section=feed_space["section"],
        bathrooms=feed_space["bathrooms"],
        living_area=feed_space["living_area"],
        kitchen_area=feed_space["kitchen_area"],
        delivery_quarter=feed_space["delivery_quarter"],
        mortgage_monthly=feed_space["mortgage_monthly"],
        mortgage_rate=feed_space["mortgage_rate"],
        installment_initial=feed_space["installment_initial"],
        price=PriceSchema(
            amount=price["amount"],
            currency=price["currency"],
        ),
        status=feed_space["status"],
        delivery_status=feed_space["delivery_status"],
        images=feed_space["images"],
        badges=feed_space["badges"],
        finishing=feed_space["finishing"],
        purchase_methods=feed_space["purchase_methods"],
        promotions=feed_space["promotions"],
        spaces=feed_space["spaces"],
        window_views=feed_space["window_views"],
        layout_features=feed_space["layout_features"],
    )


async def get_spaces() -> list[SpaceSchema]:
    feed_spaces = await get_feed_spaces()
    feed_buildings = await get_feed_buildings()
    feed_complexes = await get_feed_complexes()
    buildings_by_id = {building["id"]: building for building in feed_buildings}
    complexes_by_id = {complex["id"]: complex for complex in feed_complexes}

    return [
        map_feed_space_to_schema(feed_space, buildings_by_id, complexes_by_id)
        for feed_space in feed_spaces
    ]


async def get_space(space_id: str) -> SpaceSchema | None:
    spaces = await get_spaces()

    return next((space for space in spaces if space.id == space_id), None)


def unique_sorted(values: list[str]) -> list[str]:
    return sorted(set(values))


async def get_space_filters_meta() -> SpaceFiltersMetaSchema:
    spaces = await get_spaces()

    return SpaceFiltersMetaSchema(
        stypes=unique_sorted([space.stype for space in spaces]),
        price=NumberRangeSchema(
            min=min(space.price.amount for space in spaces),
            max=max(space.price.amount for space in spaces),
        ),
        area=NumberRangeSchema(
            min=min(space.area for space in spaces),
            max=max(space.area for space in spaces),
        ),
        floor=NumberRangeSchema(
            min=min(space.floor for space in spaces),
            max=max(space.floor for space in spaces),
        ),
        bathrooms=sorted(set(space.bathrooms for space in spaces)),
        finishing=unique_sorted([space.finishing for space in spaces]),
        delivery_statuses=unique_sorted([space.delivery_status for space in spaces]),
        purchase_methods=unique_sorted([value for space in spaces for value in space.purchase_methods]),
        promotions=unique_sorted([value for space in spaces for value in space.promotions]),
        spaces=unique_sorted([value for space in spaces for value in space.spaces]),
        window_views=unique_sorted([value for space in spaces for value in space.window_views]),
        layout_features=unique_sorted([value for space in spaces for value in space.layout_features]),
    )
