from app.modules.theme.schemas import ThemeConfigSchema


THEME_CONFIG = ThemeConfigSchema(
    primaryColor="#1f6feb",
    logo="",
    typography="Inter",
    cardStyle="default",
)


async def get_theme_config(tenant_id: str) -> ThemeConfigSchema:
    return THEME_CONFIG
