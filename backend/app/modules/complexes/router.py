from fastapi import APIRouter, HTTPException

from app.modules.complexes.repository import get_complex_summaries, get_complex_summary
from app.modules.complexes.schemas import ComplexSummarySchema
from app.modules.developers.repository import get_developer_by_slug

router = APIRouter(prefix="/api/complexes", tags=["complexes"])


@router.get("", response_model=list[ComplexSummarySchema])
async def list_complexes(developer: str | None = None) -> list[ComplexSummarySchema]:
    developer_id: str | None = None

    if developer is not None:
        resolved = await get_developer_by_slug(developer)

        if resolved is None:
            return []

        developer_id = resolved.id

    return await get_complex_summaries(developer_id)


@router.get("/{complex_id}", response_model=ComplexSummarySchema)
async def retrieve_complex(complex_id: str) -> ComplexSummarySchema:
    complex = await get_complex_summary(complex_id)

    if complex is None:
        raise HTTPException(status_code=404, detail="Complex not found")

    return complex
