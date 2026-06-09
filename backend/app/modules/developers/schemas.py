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


class DeveloperUpdateSchema(BaseModel):
    """Editable fields exposed in the admin panel.

    Covers basic info (name, slug, phone, logo) plus global styles
    (theme_config). `id` and `domains` are not editable in the basic version.
    """

    name: str
    slug: str
    logo: str
    phone: str
    theme_config: ThemeConfigSchema
