from typing import Literal

from pydantic import BaseModel

PlanKind = Literal["masterplan", "building", "floor"]
PlanRegionTargetKind = Literal["building", "floor", "space"]


class PlanAssetSchema(BaseModel):
    id: str
    complex_id: str
    kind: PlanKind
    target_id: str
    image_url: str
    width: int
    height: int


class PlanRegionSchema(BaseModel):
    id: str
    asset_id: str
    points: list[list[float]]
    target_kind: PlanRegionTargetKind
    target_id: str
    label: str
    status: str
