from fastapi import APIRouter, HTTPException

from app.modules.admin.schemas import AdminLoginRequest, AdminTokenSchema
from app.modules.admin.security import issue_token, verify_password

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/login", response_model=AdminTokenSchema)
async def login(request: AdminLoginRequest) -> AdminTokenSchema:
    if not verify_password(request.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    return AdminTokenSchema(token=issue_token())
