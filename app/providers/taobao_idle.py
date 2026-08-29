"""TOP 签名调用。未配置凭据时明确失败，不伪造商品。"""

from __future__ import annotations

import hashlib
import json
import time
from typing import Any

import httpx

from app.config import settings


class MissingCredentials(RuntimeError):
    pass


def _sign(params: dict[str, str], secret: str) -> str:
    pieces = secret + "".join(f"{k}{params[k]}" for k in sorted(params)) + secret
    return hashlib.md5(pieces.encode("utf-8")).hexdigest().upper()


def query_materials(
    keyword: str,
    page_num: int = 1,
    page_size: int = 10,
    item_publisher_time: str = "in1day",
) -> dict[str, Any]:
    if not (settings.taobao_app_key and settings.taobao_app_secret and settings.taobao_session_key):
        raise MissingCredentials("缺少 TAOBAO_APP_KEY / APP_SECRET / SESSION_KEY")

    vo = {
        "materialType": 1,
        "pageRequest": {"pageNum": page_num, "pageSize": page_size},
        "itemGuideVO": {
            "keyword": keyword,
            "itemPublisherTime": item_publisher_time,
        },
    }
    params = {
        "method": "alibaba.idle.affiliate.material.query",
        "app_key": settings.taobao_app_key,
        "session": settings.taobao_session_key,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "format": "json",
        "v": "2.0",
        "sign_method": "md5",
        "materials_query_vo": json.dumps(vo, ensure_ascii=False, separators=(",", ":")),
    }
    params["sign"] = _sign(params, settings.taobao_app_secret)
    with httpx.Client(timeout=20.0) as client:
        r = client.post(settings.taobao_gateway, data=params)
        r.raise_for_status()
        return r.json()
