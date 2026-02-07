"""Pydantic models for URL shortener."""
from pydantic import BaseModel, HttpUrl, field_validator


class URLRequest(BaseModel):
	url: HttpUrl

	@field_validator("url", mode="before")
	@classmethod
	def strip_and_validate_url(cls, value: str) -> str:
		if value is None:
			raise ValueError("URL is required")
		if isinstance(value, str):
			stripped = value.strip()
			if not stripped:
				raise ValueError("URL cannot be empty")
			return stripped
		return value


class URLResponse(BaseModel):
	short_code: str
	short_url: str

