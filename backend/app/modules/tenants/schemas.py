from pydantic import BaseModel

from app.modules.developers.schemas import DeveloperSchema
from app.modules.theme.schemas import ThemeConfigSchema

__all__ = ["DeveloperSchema", "TenantSchema"]


class TenantSchema(BaseModel):
    id: str
    developer: DeveloperSchema
    domain: str
    theme_config: ThemeConfigSchema
