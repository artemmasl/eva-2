from fastapi import APIRouter, HTTPException

from app.modules.tenants.repository import (
    get_tenant,
    get_tenant_by_domain,
    get_tenant_by_slug,
)
from app.modules.tenants.schemas import TenantSchema

router = APIRouter(prefix="/api/tenants", tags=["tenants"])


@router.get("/by-domain", response_model=TenantSchema)
async def retrieve_tenant_by_domain(domain: str) -> TenantSchema:
    tenant = await get_tenant_by_domain(domain)

    if tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")

    return tenant


@router.get("/by-developer/{slug}", response_model=TenantSchema)
async def retrieve_tenant_by_developer(slug: str) -> TenantSchema:
    tenant = await get_tenant_by_slug(slug)

    if tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")

    return tenant


@router.get("/{tenant_id}", response_model=TenantSchema)
async def retrieve_tenant(tenant_id: str) -> TenantSchema:
    tenant = await get_tenant(tenant_id)

    if tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")

    return tenant
