from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import engine, Base
from app.api.routes import health, segment, history, metrics
from app.core.logging import setup_logging
from app.core.config import settings

app = FastAPI(title="Khmer Space Injector API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,  # from .env
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    setup_logging()
    if settings.ENV != "production":
        Base.metadata.create_all(bind=engine)

app.include_router(health.router)
app.include_router(segment.router)
app.include_router(history.router)
app.include_router(metrics.router)
