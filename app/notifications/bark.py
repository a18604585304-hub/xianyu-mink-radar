"""Bark 推送。密钥只从环境变量读取，日志里只打 HTTP 状态，不打 Key。"""

from __future__ import annotations

import logging
from urllib.parse import quote

import httpx

from app.config import settings

log = logging.getLogger(__name__)


class BarkError(RuntimeError):
    pass


def _keys() -> list[str]:
    keys = [settings.bark_key, settings.bark_key_2]
    return [k.strip() for k in keys if k and k.strip()]


def send(
    title: str,
    body: str = "",
    url: str | None = None,
    group: str = "xianyu-mink-radar",
    retries: int = 2,
) -> list[int]:
    keys = _keys()
    if not keys:
        raise BarkError("缺少 BARK_KEY")

    base = settings.bark_server.rstrip("/")
    statuses: list[int] = []
    for key in keys:
        endpoint = f"{base}/{key}/{quote(title)}"
        params: dict[str, str] = {"group": group}
        if body:
            params["body"] = body
        if url:
            params["url"] = url
        last_exc: Exception | None = None
        status = 0
        for attempt in range(retries + 1):
            try:
                with httpx.Client(timeout=15.0) as client:
                    r = client.get(endpoint, params=params)
                    status = r.status_code
                    if r.status_code == 200:
                        break
                    last_exc = BarkError(f"bark http {r.status_code}")
            except Exception as e:  # noqa: BLE001 — 网络抖动后重试
                last_exc = e
                status = 0
            log.warning("bark retry %s status=%s", attempt, status)
        statuses.append(status)
        if last_exc and status != 200:
            log.error("bark failed after retries status=%s", status)
    return statuses
