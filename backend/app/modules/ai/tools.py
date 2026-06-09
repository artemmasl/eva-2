import json

from app.modules.complexes.repository import get_complex_summaries
from app.modules.spaces.repository import get_space, get_spaces
from app.modules.spaces.schemas import SpaceSchema

TOOLS: list[dict] = [
    {
        "type": "function",
        "function": {
            "name": "search_spaces",
            "description": (
                "Найти квартиры/помещения в продаже по фильтрам. "
                "Используй, когда пользователь ищет варианты по параметрам "
                "(комнаты, цена, площадь, этаж, ЖК)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "complex_id": {
                        "type": "string",
                        "description": "ID жилого комплекса для ограничения поиска",
                    },
                    "stype": {
                        "type": "string",
                        "enum": ["flat", "parking", "storage", "commercial"],
                        "description": "Тип помещения (flat = квартира)",
                    },
                    "rooms": {
                        "type": "integer",
                        "description": "Количество комнат (0 = студия)",
                    },
                    "price_min": {"type": "integer", "description": "Минимальная цена, руб"},
                    "price_max": {"type": "integer", "description": "Максимальная цена, руб"},
                    "area_min": {"type": "number", "description": "Минимальная площадь, м²"},
                    "area_max": {"type": "number", "description": "Максимальная площадь, м²"},
                    "limit": {
                        "type": "integer",
                        "description": "Сколько вариантов вернуть (по умолчанию 5)",
                    },
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_complexes",
            "description": (
                "Получить список жилых комплексов застройщика со статистикой "
                "(сколько квартир в продаже, цена от). Используй для общих вопросов о ЖК."
            ),
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_space_details",
            "description": "Получить подробную информацию о конкретной квартире/помещении по её ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "space_id": {"type": "string", "description": "ID помещения"},
                },
                "required": ["space_id"],
            },
        },
    },
]


def _space_brief(space: SpaceSchema) -> dict:
    rooms_label = "студия" if space.rooms == 0 else f"{space.rooms}-комн"

    return {
        "id": space.id,
        "complex_id": space.complex_id,
        "complex_name": space.complex_name,
        "building_name": space.building_name,
        "stype": space.stype,
        "rooms": rooms_label,
        "area": space.area,
        "floor": space.floor,
        "floors_total": space.floors_total,
        "price": space.price.amount,
        "finishing": space.finishing,
        "status": space.status,
        "delivery_quarter": space.delivery_quarter,
        "address": space.building_address,
        "district": space.building_district,
        "metro": space.building_metro,
        "metro_time": space.building_metro_time,
    }


async def _search_spaces(args: dict) -> dict:
    spaces = await get_spaces()
    spaces = [space for space in spaces if space.status == "available"]

    complex_id = args.get("complex_id")
    stype = args.get("stype")
    rooms = args.get("rooms")
    price_min = args.get("price_min")
    price_max = args.get("price_max")
    area_min = args.get("area_min")
    area_max = args.get("area_max")

    if complex_id is not None:
        spaces = [s for s in spaces if s.complex_id == complex_id]
    if stype is not None:
        spaces = [s for s in spaces if s.stype == stype]
    if rooms is not None:
        spaces = [s for s in spaces if s.rooms == rooms]
    if price_min is not None:
        spaces = [s for s in spaces if s.price.amount >= price_min]
    if price_max is not None:
        spaces = [s for s in spaces if s.price.amount <= price_max]
    if area_min is not None:
        spaces = [s for s in spaces if s.area >= area_min]
    if area_max is not None:
        spaces = [s for s in spaces if s.area <= area_max]

    spaces.sort(key=lambda s: s.price.amount)

    limit = args.get("limit") or 5
    limit = max(1, min(int(limit), 20))
    total = len(spaces)

    return {
        "total": total,
        "items": [_space_brief(space) for space in spaces[:limit]],
    }


async def _list_complexes(_args: dict) -> dict:
    summaries = await get_complex_summaries()

    return {
        "items": [
            {
                "id": summary.id,
                "name": summary.name,
                "address": summary.address,
                "district": summary.district,
                "metro": summary.metro,
                "metro_time": summary.metro_time,
                "delivery_status": summary.delivery_status,
                "coordinates": {
                    "lat": summary.coordinates.lat,
                    "lng": summary.coordinates.lng,
                },
                "flats_for_sale": summary.stats.flats_for_sale,
                "price_from": summary.stats.price_from,
            }
            for summary in summaries
        ]
    }


async def _get_space_details(args: dict) -> dict:
    space_id = args.get("space_id")

    if not space_id:
        return {"error": "space_id обязателен"}

    space = await get_space(space_id)

    if space is None:
        return {"error": "Помещение не найдено"}

    brief = _space_brief(space)
    brief.update(
        {
            "living_area": space.living_area,
            "kitchen_area": space.kitchen_area,
            "bathrooms": space.bathrooms,
            "section": space.section,
            "address": space.building_address,
            "metro": space.building_metro,
            "metro_time": space.building_metro_time,
            "mortgage_monthly": space.mortgage_monthly,
            "mortgage_rate": space.mortgage_rate,
            "promotions": space.promotions,
            "window_views": space.window_views,
            "layout_features": space.layout_features,
        }
    )

    return brief


_HANDLERS = {
    "search_spaces": _search_spaces,
    "list_complexes": _list_complexes,
    "get_space_details": _get_space_details,
}


async def execute_tool(name: str, arguments: str) -> str:
    handler = _HANDLERS.get(name)

    if handler is None:
        return json.dumps({"error": f"Неизвестный инструмент: {name}"}, ensure_ascii=False)

    try:
        args = json.loads(arguments) if arguments else {}
    except json.JSONDecodeError:
        args = {}

    result = await handler(args)

    return json.dumps(result, ensure_ascii=False)
