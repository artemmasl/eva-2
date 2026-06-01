from fastapi import APIRouter

from app.modules.theme.repository import get_theme_config
from app.modules.theme.schemas import ThemeConfigSchema

router = APIRouter(prefix="/api/theme", tags=["theme"])


@router.get("/{tenant_id}", response_model=ThemeConfigSchema)
async def retrieve_theme_config(tenant_id: str) -> ThemeConfigSchema:
    return await get_theme_config(tenant_id)
