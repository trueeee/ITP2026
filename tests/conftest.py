from __future__ import annotations

import datetime as dt
from typing import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db import get_session
from app.main import app
from app.models import Base, EmissionFactor


@pytest.fixture()
def db_session() -> Iterator[Session]:
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, future=True)
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    # Seed: några emissionsfaktorer
    db.add_all(
        [
            EmissionFactor(category="travel", key="car", unit="km", co2e_per_unit=0.2, source="test"),
            EmissionFactor(category="travel", key="train", unit="km", co2e_per_unit=0.02, source="test"),
            EmissionFactor(category="food", key="beef", unit="portion", co2e_per_unit=5.0, source="test"),
        ]
    )
    db.commit()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(db_session: Session) -> Iterator[TestClient]:
    def _override_get_session() -> Iterator[Session]:
        yield db_session

    app.dependency_overrides[get_session] = _override_get_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()