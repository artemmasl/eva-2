from fastapi import APIRouter, Depends

from app.modules.admin.security import require_admin
from app.modules.leads.repository import create_lead, list_leads
from app.modules.leads.schemas import LeadCreateSchema, LeadSchema

router = APIRouter(prefix="/api/leads", tags=["leads"])


@router.post("", response_model=LeadSchema, status_code=201)
async def submit_lead(payload: LeadCreateSchema) -> LeadSchema:
    return await create_lead(payload)


@router.get("", response_model=list[LeadSchema], dependencies=[Depends(require_admin)])
async def list_all_leads() -> list[LeadSchema]:
    return await list_leads()
