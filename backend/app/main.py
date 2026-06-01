from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.modules.buildings.router import router as buildings_router
from app.modules.complexes.router import router as complexes_router
from app.modules.feed.router import router as feed_router
from app.modules.plans.router import router as plans_router
from app.modules.spaces.router import router as spaces_router
from app.modules.tenants.router import router as tenants_router
from app.modules.theme.router import router as theme_router

app = FastAPI(title="EVA-2 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(tenants_router)
app.include_router(complexes_router)
app.include_router(buildings_router)
app.include_router(spaces_router)
app.include_router(plans_router)
app.include_router(theme_router)
app.include_router(feed_router)
