import json
from collections.abc import AsyncGenerator
from datetime import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import async_session, engine
from app.main import app as fastapi_app
from app.models import Base, Code, ShiftTask


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():

    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    shift_tasks = open_mock_json("tasks")
    codes = open_mock_json("codes")

    for code in codes:
        if code["aggregated_at"] is not None:
            aggregated_at_str = code["aggregated_at"]
            code["aggregated_at"] = datetime.strptime(
                aggregated_at_str,
                "%Y-%m-%dT%H:%M:%S",
            )

    for task in shift_tasks:
        date_str = task["batch_date"]
        task["batch_date"] = datetime.strptime(date_str, "%Y-%m-%d").date()

        date_started_str = task["date_started_shift"]
        task["date_started_shift"] = datetime.strptime(
            date_started_str,
            "%Y-%m-%dT%H:%M:%S%z",
        )

        date_end_str = task["date_end_shift"]
        task["date_end_shift"] = datetime.strptime(
            date_end_str,
            "%Y-%m-%dT%H:%M:%S%z",
        )

        if task["closed_at"] is not None:
            closed_at_str = task["closed_at"]
            task["closed_at"] = datetime.strptime(
                closed_at_str,
                "%Y-%m-%dT%H:%M:%S",
            )

    async with async_session() as session:
        add_shift_tasks = insert(ShiftTask).values(shift_tasks)
        add_codes = insert(Code).values(codes)

        await session.execute(add_shift_tasks)
        await session.execute(add_codes)

        await session.commit()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
async def session_fake() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
