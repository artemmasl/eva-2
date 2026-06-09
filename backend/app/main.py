from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.modules.admin.router import router as admin_router
from app.modules.ai.router import router as ai_router
from app.modules.buildings.router import router as buildings_router
from app.modules.complexes.router import router as complexes_router
from app.modules.developers.repository import seed_developers
from app.modules.developers.router import router as developers_router
from app.modules.feed.router import router as feed_router
from app.modules.plans.router import router as plans_router
from app.modules.spaces.router import router as spaces_router
from app.modules.tenants.router import router as tenants_router
from app.modules.theme.router import router as theme_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await seed_developers()
    yield


app = FastAPI(title="EVA-2 API", lifespan=lifespan)

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


app.include_router(admin_router)
app.include_router(developers_router)
app.include_router(tenants_router)
app.include_router(complexes_router)
app.include_router(buildings_router)
app.include_router(spaces_router)
app.include_router(plans_router)
app.include_router(theme_router)
app.include_router(feed_router)
app.include_router(ai_router)
