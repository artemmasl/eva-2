from fastapi import APIRouter

from app.modules.buildings.repository import get_buildings
from app.modules.buildings.schemas import BuildingSchema

router = APIRouter(prefix="/api/buildings", tags=["buildings"])


@router.get("", response_model=list[BuildingSchema])
async def list_buildings() -> list[BuildingSchema]:
    return await get_buildings()
