import json
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from main import app
from sqlmodel import SQLModel
from sqlmodel.pool import StaticPool
from db import get_session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from models import Book
import asyncio


@pytest_asyncio.fixture(name="session")
async def session_fixture():
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
async def get_store_book_fixture(session: AsyncSession):
    stored_book = {"title": "Book 1", "description": "Detective", "pages": 300}
    book = Book(**stored_book)
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return json.loads(book.json())


@pytest.fixture(name="client")
def client_fixture(session: AsyncSession):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_book(client: TestClient, session: AsyncSession):
    book_data = {"title": "Book 2", "description": "Detective", "pages": 300}
    response = client.post("/book/", json=book_data)
    assert response.status_code == 201
    id_ = response.json().get("id")
    created_book = asyncio.run(session.get(Book, id_)).dict()
    for key in book_data.keys():
        assert created_book.get(key) == book_data.get(key)
    assert created_book.get("id") == id_


def test_read_book(client: TestClient, stored_book):
    id_ = stored_book.get("id")
    response = client.get(f"/book/{id_}")
    retrieved_book = response.json()
    assert response.status_code == 200
    for key in retrieved_book.keys():
        assert retrieved_book.get(key) == stored_book.get(key)


def test_update_book(client: TestClient, stored_book):
    id_ = stored_book.get("id")
    book_data = {"title": "Book 3", "description": "True Detective", "pages": 350}
    response = client.put(f"/book/{id_}", json=book_data)
    assert response.status_code == 200
    updated_book = response.json()
    for key in book_data.keys():
        assert book_data.get(key) == updated_book.get(key)
        assert stored_book.get(key) != updated_book.get(key)
    assert updated_book.get("id") == stored_book.get("id")


def test_delete_book(client: TestClient, session: AsyncSession, stored_book):
    id_ = stored_book.get("id")
    response = client.delete(f"/book/{id_}")
    assert response.status_code == 204
    assert asyncio.run(session.get(Book, id_)) is None
