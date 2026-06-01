from pydantic import BaseModel


class CoordinatesSchema(BaseModel):
    lat: float
    lng: float


class ComplexSchema(BaseModel):
    id: str
    developer_id: str
    name: str
    address: str
    district: str
    metro: str
    metro_time: str
    delivery_status: str
    coordinates: CoordinatesSchema


class RoomGroupStatSchema(BaseModel):
    key: str
    label: str
    count: int
    area_from: float
    price_from: int


class ComplexStatsSchema(BaseModel):
    flats_for_sale: int
    spaces_for_sale: int
    price_from: int | None
    room_groups: list[RoomGroupStatSchema]


class ComplexSummarySchema(ComplexSchema):
    stats: ComplexStatsSchema
