from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Item(Base):
    __tablename__ = "items"
    __table_args__ = (UniqueConstraint("item_id", name="uq_item_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    item_id: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    original_price: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    image_urls: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    create_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    first_seen_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_seen_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    seller_credit: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    matched_keywords: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    push_status: Mapped[str] = mapped_column(String(16), default="pending")
    push_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    item_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    deeplink: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    discovery_delay: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
