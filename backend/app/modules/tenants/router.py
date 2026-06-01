from fastapi import APIRouter, HTTPException

from app.modules.tenants.repository import get_tenant, get_tenant_by_domain
from app.modules.tenants.schemas import TenantSchema

router = APIRouter(prefix="/api/tenants", tags=["tenants"])


@router.get("/by-domain", response_model=TenantSchema)
async def retrieve_tenant_by_domain(domain: str) -> TenantSchema:
    return await get_tenant_by_domain(domain)


@router.get("/{tenant_id}", response_model=TenantSchema)
async def retrieve_tenant(tenant_id: str) -> TenantSchema:
    tenant = await get_tenant(tenant_id)

    if tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")

    return tenant
