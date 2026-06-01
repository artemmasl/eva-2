from pydantic import BaseModel


class CoordinatesSchema(BaseModel):
    lat: float
    lng: float


class BuildingSchema(BaseModel):
    id: str
    complex_id: str
    developer_id: str
    name: str
    address: str
    coordinates: CoordinatesSchema
