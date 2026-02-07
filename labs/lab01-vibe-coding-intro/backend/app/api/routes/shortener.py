"""URL shortener routes."""
import aiosqlite
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from app.db.models import fetch_by_code
from app.db.session import get_db
from app.schemas.url import URLRequest, URLResponse
from app.services.shortener import build_short_url, get_or_create_short_code

router = APIRouter()


@router.post("/shorten", response_model=URLResponse)
async def shorten_url(
	payload: URLRequest, db: aiosqlite.Connection = Depends(get_db)
) -> URLResponse:
	short_code = await get_or_create_short_code(db, str(payload.url))
	return URLResponse(short_code=short_code, short_url=build_short_url(short_code))


@router.get("/{short_code}")
async def redirect_short_url(
	short_code: str, db: aiosqlite.Connection = Depends(get_db)
) -> RedirectResponse:
	row = await fetch_by_code(db, short_code)
	if not row:
		raise HTTPException(status_code=404, detail="Short code not found")
	return RedirectResponse(url=row["long_url"], status_code=307)

