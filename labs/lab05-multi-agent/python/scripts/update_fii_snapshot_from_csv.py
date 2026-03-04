#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import unicodedata
from datetime import date
from pathlib import Path
from typing import Any


CSV_PATH = Path("/Users/silvagpe/Downloads/FIIs - lista investidor 10 - Página1.csv")
SNAPSHOT_PATH = Path(
    "/Users/silvagpe/projetos/taller/ai_training/labs/lab05-multi-agent/python/data/snapshots/fii_snapshot.json"
)


def normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    return ascii_text.lower().strip()


def segment_slug(value: str) -> str:
    normalized = normalize_text(value)
    normalized = re.sub(r"[^a-z0-9]+", "_", normalized)
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    return normalized or "outros"


def parse_ticker_and_name(raw: str) -> tuple[str, str]:
    text = (raw or "").strip()

    # Padrão principal dos FIIs: 4 letras + 11
    match = re.match(r"^([A-Z]{4}11)(.+)$", text)
    if match:
        return match.group(1), match.group(2).strip()

    # Fallback genérico: 4 letras + 2 dígitos
    fallback = re.match(r"^([A-Z]{4}\d{2})(.+)$", text)
    if fallback:
        return fallback.group(1), fallback.group(2).strip()

    ticker = text[:6].strip()
    name = text[6:].strip() if len(text) > 6 else text
    return ticker, name


def parse_number_ptbr(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip().replace('"', "")
    if text in {"", "-"}:
        return None

    text = text.replace(".", "").replace(",", ".")
    try:
        return float(text)
    except ValueError:
        return None


def parse_percent(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip().replace('%', "").replace('"', "")
    if text in {"", "-"}:
        return None
    return parse_number_ptbr(text)


def parse_money_compact(value: Any) -> float:
    if value is None:
        return 0.0

    text = str(value).strip().replace('"', "")
    if text in {"", "-"}:
        return 0.0

    match = re.match(r"^([0-9\.,]+)\s*([BMK])$", text, re.IGNORECASE)
    if not match:
        number = parse_number_ptbr(text)
        return float(number or 0.0)

    number = parse_number_ptbr(match.group(1)) or 0.0
    unit = match.group(2).upper()
    multiplier = {"B": 1_000_000_000, "M": 1_000_000, "K": 1_000}[unit]
    return float(number * multiplier)


def map_fund_type(value: str) -> str:
    normalized = normalize_text(value)
    if "papel" in normalized:
        return "papel"
    if "tijolo" in normalized:
        return "tijolo"
    return "misto"


def map_segment(value: str) -> str:
    normalized = normalize_text(value)

    canonical = {
        "titulos e valores mobiliarios": "titulos_valores",
        "shoppings / varejo": "shoppings_varejo",
        "logistico / industria / galpoes": "logistica_industria",
        "lajes corporativas": "lajes_corporativas",
        "agencias bancarias": "agencias_bancarias",
        "fundo de infraestrutura fi-infra": "infraestrutura",
        "fundo de investimentos em participacoes fip": "fip",
        "hibrido": "hibrido",
        "fiagros": "fiagros",
        "outros": "outros",
        "hoteis": "hoteis",
        "hospitalar": "hospitalar",
        "educacional": "educacional",
        "fundo de fundos": "fundo_de_fundos",
    }
    if normalized in canonical:
        return canonical[normalized]

    if "infraestrutura" in normalized:
        return "infraestrutura"
    if "logistico" in normalized or "galpoes" in normalized:
        return "logistica_industria"
    if "shopping" in normalized or "varejo" in normalized:
        return "shoppings_varejo"
    if "titulos" in normalized or "valores mobiliarios" in normalized:
        return "titulos_valores"

    return segment_slug(value)


def load_existing_metadata(snapshot_path: Path) -> dict[str, dict[str, Any]]:
    if not snapshot_path.exists():
        return {}

    data = json.loads(snapshot_path.read_text(encoding="utf-8"))
    by_ticker: dict[str, dict[str, Any]] = {}
    for fii in data.get("fiis", []):
        ticker = fii.get("ticker")
        if ticker:
            by_ticker[ticker] = fii
    return by_ticker


def build_snapshot(csv_path: Path, snapshot_path: Path) -> dict[str, Any]:
    existing_by_ticker = load_existing_metadata(snapshot_path)
    fiis: list[dict[str, Any]] = []

    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        for index, row in enumerate(reader, start=1):
            ticker, name = parse_ticker_and_name(row.get("Ativos", ""))
            existing = existing_by_ticker.get(ticker, {})

            fii = {
                "ticker": ticker,
                "name": name,
                "fund_type": map_fund_type(row.get("Tipo de Fundo", "")),
                "segment": map_segment(row.get("Segmento", "")),
                "inception_date": existing.get("inception_date", "2015-01-01"),
                "avg_daily_volume_brl": parse_money_compact(row.get("Liquidez Diária")),
                "net_equity_brl": parse_money_compact(row.get("Patrimônio Líquido")),
                "is_top_50": index <= 50,
                "dy_12m_pct": float(parse_percent(row.get("Dividend Yield")) or 0.0),
                "dy_5y_avg_pct": parse_percent(row.get("DY Médio\n5 anos")),
                "price_to_book": float(parse_number_ptbr(row.get("P/VP")) or 0.0),
                "return_12m_pct": parse_percent(row.get("Variação 12m")),
                "return_24m_pct": parse_percent(row.get("Variação 24m")),
                "return_5y_pct": parse_percent(row.get("Variação\n5 Anos")),
                "monthly_returns_pct": existing.get("monthly_returns_pct"),
            }
            fiis.append(fii)

    return {
        "as_of": str(date.today()),
        "source": "lista_investidor_csv_v1",
        "fiis": fiis,
    }


def main() -> None:
    snapshot = build_snapshot(CSV_PATH, SNAPSHOT_PATH)
    SNAPSHOT_PATH.write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    fiis = snapshot["fiis"]
    print(f"Snapshot atualizado com {len(fiis)} FIIs em: {SNAPSHOT_PATH}")
    if fiis:
        first = fiis[0]
        print(f"Exemplo: {first['ticker']} | {first['name']}")


if __name__ == "__main__":
    main()