from typing import Callable

from app.modules.complexes.schemas import (
    ComplexSchema,
    ComplexStatsSchema,
    ComplexSummarySchema,
    CoordinatesSchema,
    RoomGroupStatSchema,
)
from app.modules.feed.demo_feed import get_feed_complexes
from app.modules.spaces.repository import get_spaces
from app.modules.spaces.schemas import SpaceSchema

RoomGroupDef = tuple[str, str, Callable[[SpaceSchema], bool]]

ROOM_GROUP_DEFS: list[RoomGroupDef] = [
    ("studio", "Студии", lambda space: space.stype == "flat" and space.rooms == 0),
    ("one", "1-комнатные", lambda space: space.stype == "flat" and space.rooms == 1),
    ("two", "2-комнатные", lambda space: space.stype == "flat" and space.rooms == 2),
    ("three", "3-комнатные", lambda space: space.stype == "flat" and space.rooms == 3),
    ("four_plus", "Свыше", lambda space: space.stype == "flat" and space.rooms >= 4),
    ("parking", "Паркинг", lambda space: space.stype == "parking"),
    ("storage", "Кладовая", lambda space: space.stype == "storage"),
    ("commercial", "Коммерция", lambda space: space.stype == "commercial"),
]


def build_complex_stats(complex_spaces: list[SpaceSchema]) -> ComplexStatsSchema:
    flats_for_sale = len([space for space in complex_spaces if space.stype == "flat"])
    price_from = min((space.price.amount for space in complex_spaces), default=None)

    room_groups: list[RoomGroupStatSchema] = []
    for key, label, predicate in ROOM_GROUP_DEFS:
        group_spaces = [space for space in complex_spaces if predicate(space)]

        if not group_spaces:
            continue

        room_groups.append(
            RoomGroupStatSchema(
                key=key,
                label=label,
                count=len(group_spaces),
                area_from=min(space.area for space in group_spaces),
                price_from=min(space.price.amount for space in group_spaces),
            )
        )

    return ComplexStatsSchema(
        flats_for_sale=flats_for_sale,
        spaces_for_sale=len(complex_spaces),
        price_from=price_from,
        room_groups=room_groups,
    )


def map_feed_complex_to_schema(feed_complex: dict) -> ComplexSchema:
    coordinates = feed_complex["coordinates"]

    return ComplexSchema(
        id=feed_complex["id"],
        developer_id=feed_complex["developer_id"],
        name=feed_complex["name"],
        address=feed_complex["address"],
        district=feed_complex["district"],
        metro=feed_complex["metro"],
        metro_time=feed_complex["metro_time"],
        delivery_status=feed_complex["delivery_status"],
        coordinates=CoordinatesSchema(
            lat=coordinates["lat"],
            lng=coordinates["lng"],
        ),
    )


async def get_complexes() -> list[ComplexSchema]:
    feed_complexes = await get_feed_complexes()

    return [map_feed_complex_to_schema(feed_complex) for feed_complex in feed_complexes]


async def get_complex_summaries() -> list[ComplexSummarySchema]:
    complexes = await get_complexes()
    spaces = await get_spaces()
    available_spaces = [space for space in spaces if space.status == "available"]

    return [
        ComplexSummarySchema(
            **complex.model_dump(),
            stats=build_complex_stats(
                [space for space in available_spaces if space.complex_id == complex.id]
            ),
        )
        for complex in complexes
    ]


async def get_complex(complex_id: str) -> ComplexSchema | None:
    complexes = await get_complexes()

    return next((complex for complex in complexes if complex.id == complex_id), None)


async def get_complex_summary(complex_id: str) -> ComplexSummarySchema | None:
    summaries = await get_complex_summaries()

    return next((summary for summary in summaries if summary.id == complex_id), None)
