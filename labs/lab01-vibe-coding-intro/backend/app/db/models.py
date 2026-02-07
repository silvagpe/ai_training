"""Database schema and queries."""
from typing import Optional

import aiosqlite

from app.db.session import get_db_path


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS urls (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	long_url TEXT NOT NULL UNIQUE,
	short_code TEXT NOT NULL UNIQUE,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


async def init_db() -> None:
	async with aiosqlite.connect(get_db_path()) as db:
		await db.execute(CREATE_TABLE_SQL)
		await db.commit()


async def fetch_by_url(db: aiosqlite.Connection, url: str) -> Optional[aiosqlite.Row]:
	cursor = await db.execute("SELECT * FROM urls WHERE long_url = ?", (url,))
	row = await cursor.fetchone()
	await cursor.close()
	return row


async def fetch_by_code(
	db: aiosqlite.Connection, short_code: str
) -> Optional[aiosqlite.Row]:
	cursor = await db.execute(
		"SELECT * FROM urls WHERE short_code = ?", (short_code,)
	)
	row = await cursor.fetchone()
	await cursor.close()
	return row


async def insert_mapping(
	db: aiosqlite.Connection, url: str, short_code: str
) -> None:
	await db.execute(
		"INSERT INTO urls (long_url, short_code) VALUES (?, ?)",
		(url, short_code),
	)
	await db.commit()

