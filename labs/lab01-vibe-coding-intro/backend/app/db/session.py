"""Database session/connection helpers."""
from pathlib import Path
from typing import AsyncGenerator

import aiosqlite

from app.core.config import settings

_DEFAULT_DB_PATH = Path(__file__).resolve().parents[2] / "urls.db"


def get_db_path() -> str:
	return settings.db_path or str(_DEFAULT_DB_PATH)


async def get_db() -> AsyncGenerator[aiosqlite.Connection, None]:
	db = await aiosqlite.connect(get_db_path())
	db.row_factory = aiosqlite.Row
	try:
		yield db
	finally:
		await db.close()

