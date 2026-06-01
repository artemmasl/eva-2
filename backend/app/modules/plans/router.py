from fastapi import APIRouter, HTTPException

from app.modules.plans.repository import get_plan_asset, get_plan_assets, get_plan_regions
from app.modules.plans.schemas import PlanAssetSchema, PlanKind, PlanRegionSchema

router = APIRouter(prefix="/api/plans", tags=["plans"])


@router.get("/assets", response_model=list[PlanAssetSchema])
async def list_plan_assets(
    complex_id: str | None = None,
    kind: PlanKind | None = None,
    target_id: str | None = None,
) -> list[PlanAssetSchema]:
    return await get_plan_assets(complex_id=complex_id, kind=kind, target_id=target_id)


@router.get("/assets/{asset_id}", response_model=PlanAssetSchema)
async def retrieve_plan_asset(asset_id: str) -> PlanAssetSchema:
    asset = await get_plan_asset(asset_id)

    if asset is None:
        raise HTTPException(status_code=404, detail="Plan asset not found")

    return asset


@router.get("/assets/{asset_id}/regions", response_model=list[PlanRegionSchema])
async def list_plan_regions(asset_id: str) -> list[PlanRegionSchema]:
    return await get_plan_regions(asset_id)
