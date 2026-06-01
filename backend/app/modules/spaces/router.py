from fastapi import APIRouter, HTTPException, Query

from app.modules.spaces.repository import get_space, get_space_filters_meta, get_spaces
from app.modules.spaces.schemas import SpaceFiltersMetaSchema, SpaceSchema, SpacesPageSchema

router = APIRouter(prefix="/api/spaces", tags=["spaces"])


@router.get("", response_model=SpacesPageSchema)
async def list_spaces(
    tenant_id: str | None = None,
    complex_id: str | None = None,
    stype: str | None = None,
    is_apartment: bool | None = None,
    rooms: int | None = None,
    price_min: int | None = None,
    price_max: int | None = None,
    area_min: float | None = None,
    area_max: float | None = None,
    building_id: str | None = None,
    floor_min: int | None = None,
    floor_max: int | None = None,
    bathrooms: int | None = None,
    finishing: str | None = None,
    delivery_status: str | None = None,
    has_discount: bool = False,
    purchase_method: str | None = None,
    promotion: str | None = None,
    space: str | None = None,
    window_view: str | None = None,
    layout_feature: str | None = None,
    exclude_first_floor: bool = False,
    exclude_last_floor: bool = False,
    search: str | None = None,
    limit: int = Query(default=24, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> SpacesPageSchema:
    spaces = await get_spaces()
    top_floor = max(space.floor for space in spaces)

    if complex_id is not None:
        spaces = [space for space in spaces if space.complex_id == complex_id]
    if stype is not None:
        spaces = [space for space in spaces if space.stype == stype]
    if is_apartment is not None:
        spaces = [space for space in spaces if space.is_apartment == is_apartment]
    if rooms is not None:
        spaces = [space for space in spaces if space.rooms == rooms]
    if price_min is not None:
        spaces = [space for space in spaces if space.price.amount >= price_min]
    if price_max is not None:
        spaces = [space for space in spaces if space.price.amount <= price_max]
    if area_min is not None:
        spaces = [space for space in spaces if space.area >= area_min]
    if area_max is not None:
        spaces = [space for space in spaces if space.area <= area_max]
    if building_id is not None:
        spaces = [space for space in spaces if space.building_id == building_id]
    if floor_min is not None:
        spaces = [space for space in spaces if space.floor >= floor_min]
    if floor_max is not None:
        spaces = [space for space in spaces if space.floor <= floor_max]
    if bathrooms is not None:
        spaces = [space for space in spaces if space.bathrooms == bathrooms]
    if finishing is not None:
        spaces = [space for space in spaces if space.finishing == finishing]
    if delivery_status is not None:
        spaces = [space for space in spaces if space.delivery_status == delivery_status]
    if has_discount:
        spaces = [space for space in spaces if any("скидк" in promotion.lower() for promotion in space.promotions)]
    if purchase_method is not None:
        spaces = [space for space in spaces if purchase_method in space.purchase_methods]
    if promotion is not None:
        spaces = [space for space in spaces if promotion in space.promotions]
    if space is not None:
        spaces = [item for item in spaces if space in item.spaces]
    if window_view is not None:
        spaces = [space for space in spaces if window_view in space.window_views]
    if layout_feature is not None:
        spaces = [space for space in spaces if layout_feature in space.layout_features]
    if exclude_first_floor:
        spaces = [space for space in spaces if space.floor > 1]
    if exclude_last_floor:
        spaces = [space for space in spaces if space.floor < top_floor]
    if search:
        normalized_search = search.lower()
        spaces = [space for space in spaces if normalized_search in space.id.lower()]

    total = len(spaces)
    page_items = spaces[offset : offset + limit]

    return SpacesPageSchema(
        items=page_items,
        total=total,
        limit=limit,
        offset=offset,
        has_more=offset + limit < total,
    )


@router.get("/filters", response_model=SpaceFiltersMetaSchema)
async def retrieve_space_filters() -> SpaceFiltersMetaSchema:
    return await get_space_filters_meta()


@router.get("/{space_id}", response_model=SpaceSchema)
async def retrieve_space(space_id: str) -> SpaceSchema:
    space = await get_space(space_id)

    if space is None:
        raise HTTPException(status_code=404, detail="Space not found")

    return space
