from app.modules.tenants.schemas import DeveloperSchema, TenantSchema
from app.modules.theme.repository import THEME_CONFIG


TENANT = TenantSchema(
    id="tenant-1",
    domain="localhost",
    theme_config=THEME_CONFIG,
    developer=DeveloperSchema(
        id="developer-1",
        name="СК «Атлас девелопмент»",
        slug="allio-demo",
        logo="",
        phone="+7 (343) 364-56-59",
        domains=["localhost"],
        theme_config=THEME_CONFIG,
    ),
)


async def get_tenant_by_domain(domain: str) -> TenantSchema:
    return TENANT


async def get_tenant(tenant_id: str) -> TenantSchema | None:
    if tenant_id == TENANT.id:
        return TENANT

    return None
