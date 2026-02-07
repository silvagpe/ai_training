"""Application configuration."""
from dataclasses import dataclass, field
from os import getenv
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")


@dataclass(frozen=True)
class Settings:
	base_url: str = getenv("BASE_URL", "http://localhost:8000")
	db_path: str = getenv("DATABASE_URL", "")
	allow_origins: list[str] = field(
		default_factory=lambda: getenv("ALLOW_ORIGINS", "*").split(",")
	)

	@property
	def normalized_base_url(self) -> str:
		return self.base_url.rstrip("/")


settings = Settings()

