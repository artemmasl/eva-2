from typing import TypedDict


class FeedCoordinates(TypedDict):
    lat: float
    lng: float


class FeedComplex(TypedDict):
    id: str
    developer_id: str
    name: str
    address: str
    district: str
    metro: str
    metro_time: str
    delivery_status: str
    coordinates: FeedCoordinates


class FeedBuilding(TypedDict):
    id: str
    complex_id: str
    developer_id: str
    name: str
    address: str
    district: str
    metro: str
    metro_time: str
    coordinates: FeedCoordinates


class FeedPrice(TypedDict):
    amount: int
    currency: str


class FeedSpace(TypedDict):
    id: str
    building_id: str
    stype: str
    is_apartment: bool
    rooms: int
    area: float
    floor: int
    bathrooms: int
    living_area: float
    kitchen_area: float
    section: int
    floors_total: int
    delivery_quarter: str
    mortgage_monthly: int
    mortgage_rate: float
    installment_initial: int
    price: FeedPrice
    status: str
    delivery_status: str
    images: list[str]
    badges: list[str]
    finishing: str
    purchase_methods: list[str]
    promotions: list[str]
    spaces: list[str]
    window_views: list[str]
    layout_features: list[str]


TEST_FEED_COMPLEXES: list[FeedComplex] = [
    {
        "id": "complex-1",
        "developer_id": "developer-1",
        "name": "ЖК Атлас люкс",
        "address": "Центральный район, ул. Петрова, 28",
        "district": "Богдановский лес",
        "metro": "Метро Котельники",
        "metro_time": "20 мин. на авто",
        "delivery_status": "Строится",
        "coordinates": {"lat": 55.7558, "lng": 37.6173},
    },
    {
        "id": "complex-2",
        "developer_id": "developer-1",
        "name": "Нобель",
        "address": "Новый корпус легендарного комплекса",
        "district": "Парковый квартал",
        "metro": "Метро Ботаническая",
        "metro_time": "12 мин. пешком",
        "delivery_status": "Сдан",
        "coordinates": {"lat": 55.7612, "lng": 37.6241},
    },
]

TEST_FEED_BUILDINGS: list[FeedBuilding] = [
    {
        "id": "building-1",
        "complex_id": "complex-1",
        "developer_id": "developer-1",
        "name": "Корпус 1",
        "address": "Центральный район, ул. Петрова, 28",
        "district": "Богдановский лес",
        "metro": "Метро Котельники",
        "metro_time": "20 мин. на авто",
        "coordinates": {"lat": 55.7558, "lng": 37.6173},
    },
    {
        "id": "building-2",
        "complex_id": "complex-2",
        "developer_id": "developer-1",
        "name": "Корпус 1",
        "address": "Новый корпус легендарного комплекса",
        "district": "Парковый квартал",
        "metro": "Метро Ботаническая",
        "metro_time": "12 мин. пешком",
        "coordinates": {"lat": 55.7612, "lng": 37.6241},
    },
]

BADGE_SETS = [
    ["Выгодная ипотека", "Без оплаты"],
    ["Предчистовая отделка"],
    ["Чистовая отделка"],
    ["Без оплаты"],
    ["Новинка", "Выгодная ипотека"],
    ["Семейная ипотека"],
]

FINISHING_OPTIONS = ["Без отделки", "Предчистовая", "Чистовая", "Дизайнерская"]
PURCHASE_METHOD_OPTIONS = ["Оплата 100%", "Семейная ипотека 5%", "IT-ипотека", "Рассрочка"]
PROMOTION_OPTIONS = ["Акции месяца", "Скидка при 100% оплате", "Кухня в подарок", "Без оплаты"]
DELIVERY_STATUS_OPTIONS = ["Сдан", "Строится"]
SPACE_OPTIONS = ["Гардеробная", "Постирочная", "Мастер-спальня", "Большой балкон", "Терраса"]
WINDOW_VIEW_OPTIONS = ["На парк/лесопарк", "На воду", "На двор", "На город"]
LAYOUT_FEATURE_OPTIONS = ["2+ ванные", "Евроформат", "Угловая квартира", "Окна на две стороны"]
SPACE_TYPE_OPTIONS = ["flat", "parking", "storage", "commercial"]
DELIVERY_QUARTER_OPTIONS = ["I квартал 2027", "II квартал 2027", "IV квартал 2026"]

ROOM_AREA_MAP = {
    1: [40, 44, 52, 61],
    2: [58, 64, 72, 78],
    3: [82, 91, 104, 118],
    4: [155, 180, 200, 250],
}


def build_feed_space(index: int) -> FeedSpace:
    stype = SPACE_TYPE_OPTIONS[index % len(SPACE_TYPE_OPTIONS)]
    is_apartment = stype == "flat" and index % 8 == 0
    rooms = [1, 2, 3, 4][index % 4] if stype == "flat" else 0
    area = ROOM_AREA_MAP[rooms][index % len(ROOM_AREA_MAP[rooms])] if stype == "flat" else 0
    floor = (index % 25) + 1 if stype == "flat" else (index % 6) + 1
    price_per_meter = 148_360 if rooms in [1, 2] else 480_000 if rooms == 4 else 114_800

    if stype == "parking":
        area = [13, 14, 15, 16, 18][index % 5]
        price_per_meter = 95_000
    elif stype == "storage":
        area = [3, 4, 5, 6, 8, 10][index % 6]
        price_per_meter = 120_000
    elif stype == "commercial":
        area = [48, 62, 78, 95, 120, 145][index % 6]
        price_per_meter = 185_000

    status = "reserved" if index % 13 == 0 else "available"
    delivery_status = DELIVERY_STATUS_OPTIONS[index % len(DELIVERY_STATUS_OPTIONS)]
    finishing = FINISHING_OPTIONS[index % len(FINISHING_OPTIONS)] if stype == "flat" else ""
    purchase_methods = [
        PURCHASE_METHOD_OPTIONS[index % len(PURCHASE_METHOD_OPTIONS)],
        PURCHASE_METHOD_OPTIONS[(index + 1) % len(PURCHASE_METHOD_OPTIONS)],
    ]
    promotions = [PROMOTION_OPTIONS[index % len(PROMOTION_OPTIONS)]] if index % 3 != 0 else []
    space_options = [
        SPACE_OPTIONS[index % len(SPACE_OPTIONS)],
        SPACE_OPTIONS[(index + 2) % len(SPACE_OPTIONS)],
    ] if stype == "flat" else []
    window_views = [WINDOW_VIEW_OPTIONS[index % len(WINDOW_VIEW_OPTIONS)]] if stype == "flat" else []
    layout_features = [
        LAYOUT_FEATURE_OPTIONS[index % len(LAYOUT_FEATURE_OPTIONS)],
        LAYOUT_FEATURE_OPTIONS[(index + 1) % len(LAYOUT_FEATURE_OPTIONS)],
    ] if stype == "flat" else []

    amount = int(area * price_per_meter)
    living_area = round(area * 0.57, 1) if stype == "flat" else 0.0
    kitchen_area = round(area * 0.13, 1) if stype == "flat" else 0.0
    section = (index % 3) + 1
    floors_total = floor + ((index % 6) + 2)
    delivery_quarter = (
        "Сдан"
        if delivery_status == "Сдан"
        else DELIVERY_QUARTER_OPTIONS[index % len(DELIVERY_QUARTER_OPTIONS)]
    )
    mortgage_monthly = round(amount * 0.0068 / 1000) * 1000
    mortgage_rate = 5.0
    installment_initial = round(amount * 0.27 / 100_000) * 100_000

    return {
        "id": f"space-{index + 1}",
        "building_id": "building-1" if index % 2 == 0 else "building-2",
        "stype": stype,
        "is_apartment": is_apartment,
        "rooms": rooms,
        "area": area,
        "floor": floor,
        "bathrooms": 2 if stype == "flat" and (rooms >= 3 or index % 5 == 0) else 1 if stype == "commercial" else 0,
        "living_area": living_area,
        "kitchen_area": kitchen_area,
        "section": section,
        "floors_total": floors_total,
        "delivery_quarter": delivery_quarter,
        "mortgage_monthly": mortgage_monthly,
        "mortgage_rate": mortgage_rate,
        "installment_initial": installment_initial,
        "price": {
            "amount": amount,
            "currency": "RUB",
        },
        "status": status,
        "delivery_status": delivery_status,
        "images": [],
        "badges": BADGE_SETS[index % len(BADGE_SETS)],
        "finishing": finishing,
        "purchase_methods": purchase_methods,
        "promotions": promotions,
        "spaces": space_options,
        "window_views": window_views,
        "layout_features": layout_features,
    }


TEST_FEED_SPACES: list[FeedSpace] = [build_feed_space(index) for index in range(95)]


async def get_feed_complexes() -> list[FeedComplex]:
    return TEST_FEED_COMPLEXES


async def get_feed_buildings() -> list[FeedBuilding]:
    return TEST_FEED_BUILDINGS


async def get_feed_spaces() -> list[FeedSpace]:
    return TEST_FEED_SPACES


class FeedPlanAsset(TypedDict):
    id: str
    complex_id: str
    kind: str  # masterplan | building | floor
    target_id: str
    image_url: str
    width: int
    height: int


class FeedPlanRegion(TypedDict):
    id: str
    asset_id: str
    points: list[list[float]]  # normalized [x, y] in 0..1
    target_kind: str  # building | floor | space
    target_id: str
    label: str
    status: str


TEST_FEED_PLAN_ASSETS: list[FeedPlanAsset] = [
    {
        "id": "plan-masterplan-complex-1",
        "complex_id": "complex-1",
        "kind": "masterplan",
        "target_id": "complex-1",
        "image_url": "",
        "width": 1600,
        "height": 900,
    },
    {
        "id": "plan-masterplan-complex-2",
        "complex_id": "complex-2",
        "kind": "masterplan",
        "target_id": "complex-2",
        "image_url": "",
        "width": 1600,
        "height": 900,
    },
    {
        "id": "plan-building-1",
        "complex_id": "complex-1",
        "kind": "building",
        "target_id": "building-1",
        "image_url": "",
        "width": 900,
        "height": 1200,
    },
    {
        "id": "plan-building-2",
        "complex_id": "complex-2",
        "kind": "building",
        "target_id": "building-2",
        "image_url": "",
        "width": 900,
        "height": 1200,
    },
    {
        "id": "plan-floor-building-1-3",
        "complex_id": "complex-1",
        "kind": "floor",
        "target_id": "building-1-floor-3",
        "image_url": "",
        "width": 1400,
        "height": 900,
    },
]


TEST_FEED_PLAN_REGIONS: list[FeedPlanRegion] = [
    {
        "id": "region-mp1-b1",
        "asset_id": "plan-masterplan-complex-1",
        "points": [[0.30, 0.25], [0.62, 0.20], [0.66, 0.70], [0.34, 0.78]],
        "target_kind": "building",
        "target_id": "building-1",
        "label": "Корпус 1",
        "status": "available",
    },
    {
        "id": "region-mp2-b2",
        "asset_id": "plan-masterplan-complex-2",
        "points": [[0.35, 0.28], [0.64, 0.24], [0.68, 0.72], [0.32, 0.78]],
        "target_kind": "building",
        "target_id": "building-2",
        "label": "Корпус 1",
        "status": "available",
    },
    {
        "id": "region-b1-f3",
        "asset_id": "plan-building-1",
        "points": [[0.20, 0.30], [0.80, 0.30], [0.80, 0.42], [0.20, 0.42]],
        "target_kind": "floor",
        "target_id": "building-1-floor-3",
        "label": "3 этаж",
        "status": "available",
    },
    {
        "id": "region-b1-f2",
        "asset_id": "plan-building-1",
        "points": [[0.20, 0.45], [0.80, 0.45], [0.80, 0.57], [0.20, 0.57]],
        "target_kind": "floor",
        "target_id": "building-1-floor-2",
        "label": "2 этаж",
        "status": "available",
    },
    {
        "id": "region-b1-f1",
        "asset_id": "plan-building-1",
        "points": [[0.20, 0.60], [0.80, 0.60], [0.80, 0.72], [0.20, 0.72]],
        "target_kind": "floor",
        "target_id": "building-1-floor-1",
        "label": "1 этаж",
        "status": "available",
    },
    {
        "id": "region-f3-s1",
        "asset_id": "plan-floor-building-1-3",
        "points": [[0.08, 0.20], [0.30, 0.20], [0.30, 0.62], [0.08, 0.62]],
        "target_kind": "space",
        "target_id": "space-1",
        "label": "",
        "status": "available",
    },
    {
        "id": "region-f3-s3",
        "asset_id": "plan-floor-building-1-3",
        "points": [[0.34, 0.20], [0.56, 0.20], [0.56, 0.62], [0.34, 0.62]],
        "target_kind": "space",
        "target_id": "space-3",
        "label": "",
        "status": "available",
    },
    {
        "id": "region-f3-s5",
        "asset_id": "plan-floor-building-1-3",
        "points": [[0.60, 0.20], [0.82, 0.20], [0.82, 0.62], [0.60, 0.62]],
        "target_kind": "space",
        "target_id": "space-5",
        "label": "",
        "status": "available",
    },
]


async def get_feed_plan_assets() -> list[FeedPlanAsset]:
    return TEST_FEED_PLAN_ASSETS


async def get_feed_plan_regions() -> list[FeedPlanRegion]:
    return TEST_FEED_PLAN_REGIONS
