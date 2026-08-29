#!/usr/bin/env python3
"""Phase 0：单次调用官方物料查询。无凭据时明确退出，不伪造结果。"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.providers.taobao_idle import MissingCredentials, query_materials  # noqa: E402


def parse_items(raw: dict) -> list[dict]:
    """字段路径以实际 JSON 为准；文档结构可能嵌套多层。"""
    found: list[dict] = []

    def walk(node):
        if isinstance(node, dict):
            if "item_id" in node or "itemId" in node:
                found.append(node)
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for x in node:
                walk(x)

    walk(raw)
    return found


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--keyword", default="抽刀貂")
    p.add_argument("--page-size", type=int, default=10)
    args = p.parse_args()
    request_time = datetime.now()
    try:
        raw = query_materials(args.keyword, page_size=args.page_size)
    except MissingCredentials as e:
        print("POC 未执行：", e)
        print("原因见 docs/OFFICIAL_API_NOTES.md：当前淘宝账号无法入驻闲鱼联盟（需企业支付宝资质）。")
        return 2
    except Exception as e:
        print("API 调用失败：", e)
        return 1

    raw_dir = ROOT / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    stamp = request_time.strftime("%Y%m%d_%H%M%S")
    out = raw_dir / f"{stamp}_{args.keyword}.json"
    out.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")
    print("raw saved:", out)

    items = parse_items(raw)
    print(f"[{request_time:%H:%M:%S}] 搜索：{args.keyword}")
    print(f"发现 {len(items)} 件含 item_id 的节点")
    print("（未假设官方排序；有 create_time 的会在下面按时间排）")

    timed = []
    for it in items:
        ct = it.get("create_time") or it.get("createTime")
        timed.append((str(ct or ""), it))
    timed.sort(key=lambda x: x[0], reverse=True)
    for ct, it in timed[:20]:
        iid = it.get("item_id") or it.get("itemId")
        title = it.get("item_title") or it.get("title") or ""
        price = it.get("reserve_price") or it.get("price") or ""
        print("-------------------")
        print(iid)
        print("标题：", title)
        print("价格：", price)
        print("发布时间：", ct)
        print("抓取时间：", request_time.strftime("%Y-%m-%d %H:%M:%S"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
