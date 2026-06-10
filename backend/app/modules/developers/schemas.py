from pydantic import BaseModel

from app.modules.theme.schemas import ThemeConfigSchema


class SocialLinksSchema(BaseModel):
    """Optional social network profile URLs shown in the storefront."""

    vk: str = ""
    ok: str = ""
    telegram: str = ""


class DeveloperSchema(BaseModel):
    id: str
    name: str
    slug: str
    logo: str
    phone: str
    email: str = ""
    website: str = ""
    socials: SocialLinksSchema = SocialLinksSchema()
    privacy_policy: str = ""
    domains: list[str]
    theme_config: ThemeConfigSchema


class DeveloperUpdateSchema(BaseModel):
    """Editable fields exposed in the admin panel.

    Covers basic info (name, slug, phone, logo, email, website, socials,
    privacy policy) plus global styles (theme_config). `id` and `domains`
    are not editable in the basic version.
    """

    name: str
    slug: str
    logo: str
    phone: str
    email: str = ""
    website: str = ""
    socials: SocialLinksSchema = SocialLinksSchema()
    privacy_policy: str = ""
    theme_config: ThemeConfigSchema
