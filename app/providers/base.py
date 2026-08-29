from __future__ import annotations

from typing import Any, Protocol


class MaterialProvider(Protocol):
    def query_materials(
        self,
        keyword: str,
        page_num: int = 1,
        page_size: int = 10,
        item_publisher_time: str = "in1day",
    ) -> dict[str, Any]:
        ...
