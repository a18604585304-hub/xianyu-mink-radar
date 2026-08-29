from __future__ import annotations

from pathlib import Path

import yaml

_CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "keywords.yaml"


def load_filter_config(path: Path | None = None) -> dict:
    p = path or _CONFIG_PATH
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def match_keywords(title: str, description: str | None, cfg: dict | None = None) -> list[str]:
    cfg = cfg or load_filter_config()
    text = f"{title or ''} {description or ''}"
    hits: list[str] = []
    for word in (cfg.get("precision") or []) + (cfg.get("broad") or []):
        if word and word in text:
            hits.append(word)
    return hits


def is_excluded(title: str, description: str | None, cfg: dict | None = None) -> bool:
    cfg = cfg or load_filter_config()
    text = f"{title or ''} {description or ''}"
    return any(word and word in text for word in (cfg.get("exclude") or []))
