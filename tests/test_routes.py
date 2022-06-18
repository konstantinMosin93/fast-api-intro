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


@pytest.fixture(name="client")
def client_fixture(session: AsyncSession):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_book(client: TestClient, session: AsyncSession):
    response = client.post(
        "/book/",
        json={"title": "Book 2", "description": "Detective", "pages": 300}
    )
    assert response.status_code == 201
    id_ = response.json().get("id")

    async def get_book():
        return await session.get(Book, id_)

    stored_book = asyncio.run(get_book()).dict()

    assert stored_book.get("title") == "Book 2"
    assert stored_book.get("description") == "Detective"
    assert stored_book.get("pages") == 300


def test_read_book(client: TestClient, session: AsyncSession):
    stored_book = {"title": "Book 3", "description": "Detective", "pages": 300}

    async def add_book():
        book = Book(**stored_book)
        session.add(book)
        await session.commit()

    asyncio.run(add_book())

    response = client.get("/book/1")
    retrieved_book = response.json()
    assert response.status_code == 200
    assert retrieved_book.get("title") == "Book 3"
    assert retrieved_book.get("description") == "Detective"
    assert retrieved_book.get("pages") == 300


def test_update_book(client: TestClient, session: AsyncSession):
    stored_book = {"title": "Book 4", "description": "Detective", "pages": 300}

    async def add_book():
        book = Book(**stored_book)
        session.add(book)
        await session.commit()

    asyncio.run(add_book())

    response = client.put(
        "/book/1",
        json={"title": "Book 5", "description": "True Detective", "pages": 350}
    )
    assert response.status_code == 200
    updated_book = response.json()
    assert updated_book.get("id") == 1
    assert stored_book.get("title") != updated_book.get("title")
    assert stored_book.get("description") != updated_book.get("description")
    assert stored_book.get("pages") != updated_book.get("pages")
    assert updated_book.get("title") == "Book 5"
    assert updated_book.get("description") == "True Detective"
    assert updated_book.get("pages") == 350


def test_delete_book(client: TestClient, session: AsyncSession):
    stored_book = {"title": "Book 6", "description": "Detective", "pages": 300}

    async def add_book():
        book = Book(**stored_book)
        session.add(book)
        await session.commit()

    asyncio.run(add_book())

    response = client.delete("/book/1")
    assert response.status_code == 204

    async def get_book():
        return await session.get(Book, 1)

    assert asyncio.run(get_book()) is None
