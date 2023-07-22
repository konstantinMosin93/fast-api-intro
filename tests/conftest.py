import json
from typing import Dict, Any

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.pool import StaticPool

from src.db import get_session
from src.main import app
from src.models import Book


@pytest_asyncio.fixture(name="session")
async def session_fixture() -> AsyncSession:
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=True) as session:
        yield session


@pytest_asyncio.fixture(name="stored_book")
async def store_book_fixture(session: AsyncSession) -> Dict[str, Any]:
    stored_book = {"title": "Book 1", "description": "Detective", "pages": 300}
    book = Book(**stored_book)
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return json.loads(book.json())


@pytest.fixture(name="client")
def client_fixture(session: AsyncSession) -> TestClient:
    def get_session_override() -> AsyncSession:
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
