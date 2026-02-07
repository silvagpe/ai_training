"""FastAPI application entrypoint."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.api.routes.shortener import router as shortener_router
from app.core.config import settings
from app.db.models import init_db

app = FastAPI(title="URL Shortener")

app.add_middleware(
	CORSMiddleware,
	allow_origins=settings.allow_origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(shortener_router)


@app.on_event("startup")
async def on_startup() -> None:
	print("[startup] BASE_URL=",settings.base_url)
	print("[startup] DATABASE_URL=", settings.db_path or "<default>")
	print("[startup] ALLOW_ORIGINS=", settings.allow_origins)
	await init_db()

