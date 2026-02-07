"""Business logic for URL shortening."""
import secrets
import string

import aiosqlite

from app.core.config import settings
from app.db.models import fetch_by_code, fetch_by_url, insert_mapping

ALPHANUMERIC = string.ascii_letters + string.digits


def generate_code(length: int = 6) -> str:
	return "".join(secrets.choice(ALPHANUMERIC) for _ in range(length))


def build_short_url(short_code: str) -> str:
	return f"{settings.normalized_base_url}/{short_code}"


async def get_or_create_short_code(
	db: aiosqlite.Connection,
	url: str,
	length: int = 6,
	max_attempts: int = 10,
) -> str:
	existing = await fetch_by_url(db, url)
	if existing:
		return existing["short_code"]

	for _ in range(max_attempts):
		short_code = generate_code(length)
		if not await fetch_by_code(db, short_code):
			await insert_mapping(db, url, short_code)
			return short_code

	raise RuntimeError("Failed to generate unique short code")

