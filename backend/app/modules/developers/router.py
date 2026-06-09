from fastapi import APIRouter, Depends, HTTPException

from app.modules.admin.security import require_admin
from app.modules.developers.repository import (
    get_developer,
    get_developer_by_slug,
    list_developers,
    update_developer,
)
from app.modules.developers.schemas import DeveloperSchema, DeveloperUpdateSchema

router = APIRouter(prefix="/api/developers", tags=["developers"])


@router.get("", response_model=list[DeveloperSchema], dependencies=[Depends(require_admin)])
async def list_all_developers() -> list[DeveloperSchema]:
    return await list_developers()


@router.get("/by-slug/{slug}", response_model=DeveloperSchema)
async def retrieve_developer_by_slug(slug: str) -> DeveloperSchema:
    developer = await get_developer_by_slug(slug)

    if developer is None:
        raise HTTPException(status_code=404, detail="Developer not found")

    return developer


@router.get("/{developer_id}", response_model=DeveloperSchema, dependencies=[Depends(require_admin)])
async def retrieve_developer(developer_id: str) -> DeveloperSchema:
    developer = await get_developer(developer_id)

    if developer is None:
        raise HTTPException(status_code=404, detail="Developer not found")

    return developer


@router.put("/{developer_id}", response_model=DeveloperSchema, dependencies=[Depends(require_admin)])
async def edit_developer(
    developer_id: str,
    payload: DeveloperUpdateSchema,
) -> DeveloperSchema:
    developer = await update_developer(developer_id, payload)

    if developer is None:
        raise HTTPException(status_code=404, detail="Developer not found")

    return developer
