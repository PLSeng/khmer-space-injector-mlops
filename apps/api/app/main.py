from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes.health import router as health_router
from app.api.routes.segment import router as segment_router
from app.api.routes.records import router as records_router

from app.services.segmenter import Segmenter
from app.main_state import set_segmenter

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load model once on startup
    seg = Segmenter.load_from_artifacts(settings.artifact_path, device=settings.DEVICE)
    set_segmenter(seg)
    yield
    # no teardown needed

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(segment_router)
app.include_router(records_router)
