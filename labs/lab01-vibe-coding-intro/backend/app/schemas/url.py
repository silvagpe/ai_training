"""Pydantic models for URL shortener."""
from pydantic import BaseModel, HttpUrl


class URLRequest(BaseModel):
	url: HttpUrl


class URLResponse(BaseModel):
	short_code: str
	short_url: str

