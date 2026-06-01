from fastapi import APIRouter, HTTPException

from app.modules.complexes.repository import get_complex_summaries, get_complex_summary
from app.modules.complexes.schemas import ComplexSummarySchema

router = APIRouter(prefix="/api/complexes", tags=["complexes"])


@router.get("", response_model=list[ComplexSummarySchema])
async def list_complexes() -> list[ComplexSummarySchema]:
    return await get_complex_summaries()


@router.get("/{complex_id}", response_model=ComplexSummarySchema)
async def retrieve_complex(complex_id: str) -> ComplexSummarySchema:
    complex = await get_complex_summary(complex_id)

    if complex is None:
        raise HTTPException(status_code=404, detail="Complex not found")

    return complex
