from app.modules.developers.repository import (
    get_developer,
    get_developer_by_domain,
    get_developer_by_slug,
)
from app.modules.developers.schemas import DeveloperSchema
from app.modules.tenants.schemas import TenantSchema


def _build_tenant(developer: DeveloperSchema) -> TenantSchema:
    domain = developer.domains[0] if developer.domains else "localhost"

    return TenantSchema(
        id=f"tenant-{developer.id}",
        domain=domain,
        theme_config=developer.theme_config,
        developer=developer,
    )


async def get_tenant_by_domain(domain: str) -> TenantSchema | None:
    developer = await get_developer_by_domain(domain)

    return _build_tenant(developer) if developer else None


async def get_tenant_by_slug(slug: str) -> TenantSchema | None:
    developer = await get_developer_by_slug(slug)

    return _build_tenant(developer) if developer else None


async def get_tenant(tenant_id: str) -> TenantSchema | None:
    developer_id = tenant_id.removeprefix("tenant-")
    developer = await get_developer(developer_id)

    return _build_tenant(developer) if developer else None
