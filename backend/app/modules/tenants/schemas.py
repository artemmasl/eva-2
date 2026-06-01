from pydantic import BaseModel

from app.modules.theme.schemas import ThemeConfigSchema


class DeveloperSchema(BaseModel):
    id: str
    name: str
    slug: str
    logo: str
    phone: str
    domains: list[str]
    theme_config: ThemeConfigSchema


class TenantSchema(BaseModel):
    id: str
    developer: DeveloperSchema
    domain: str
    theme_config: ThemeConfigSchema
