#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.notifications.bark import send  # noqa: E402


def main() -> int:
    statuses = send("闲鱼抽刀貂雷达部署测试成功", "Phase 0 Bark 连通测试")
    print("bark statuses:", statuses)
    return 0 if all(s == 200 for s in statuses) else 1


if __name__ == "__main__":
    raise SystemExit(main())
