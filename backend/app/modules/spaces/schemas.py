from pydantic import BaseModel


class PriceSchema(BaseModel):
    amount: int
    currency: str


class SpaceSchema(BaseModel):
    id: str
    complex_id: str
    complex_name: str
    building_id: str
    building_name: str
    building_address: str
    building_district: str
    building_metro: str
    building_metro_time: str
    stype: str
    is_apartment: bool
    rooms: int
    area: float
    floor: int
    floors_total: int
    section: int
    bathrooms: int
    living_area: float
    kitchen_area: float
    delivery_quarter: str
    mortgage_monthly: int
    mortgage_rate: float
    installment_initial: int
    price: PriceSchema
    status: str
    delivery_status: str
    images: list[str]
    badges: list[str] = []
    finishing: str
    purchase_methods: list[str]
    promotions: list[str]
    spaces: list[str]
    window_views: list[str]
    layout_features: list[str]


class SpacesPageSchema(BaseModel):
    items: list[SpaceSchema]
    total: int
    limit: int
    offset: int
    has_more: bool


class NumberRangeSchema(BaseModel):
    min: float
    max: float


class SpaceFiltersMetaSchema(BaseModel):
    stypes: list[str]
    price: NumberRangeSchema
    area: NumberRangeSchema
    floor: NumberRangeSchema
    bathrooms: list[int]
    finishing: list[str]
    delivery_statuses: list[str]
    purchase_methods: list[str]
    promotions: list[str]
    spaces: list[str]
    window_views: list[str]
    layout_features: list[str]
