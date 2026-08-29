from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import settings
from app.storage.models import Base


def _engine_url() -> str:
    url = settings.database_url
    if url.startswith("sqlite:///"):
        return url
    return url


engine = create_engine(_engine_url(), future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, class_=Session)


def init_db() -> None:
    Base.metadata.create_all(engine)
