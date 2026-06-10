from datetime import datetime
from typing import Literal

from pydantic import BaseModel

LeadKind = Literal["callback", "consultation", "booking", "conditions"]
LeadStatus = Literal["new", "in_progress", "done"]


class LeadCreateSchema(BaseModel):
    """Payload submitted from storefront forms (public, no auth)."""

    kind: LeadKind
    name: str = ""
    phone: str
    comment: str = ""
    developer_slug: str = ""
    complex_id: str | None = None
    space_id: str | None = None
    source_url: str = ""


class LeadSchema(LeadCreateSchema):
    id: str
    status: LeadStatus = "new"
    created_at: datetime
