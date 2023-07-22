import asyncio
from typing import Dict, Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Book


def test_create_book(client: TestClient, session: AsyncSession) -> None:
    book_data = {"title": "Book 2", "description": "Detective", "pages": 300}

    response = client.post("/book/", json=book_data)  # act

    assert response.status_code == 201
    id_ = response.json().get("id")
    created_book = asyncio.run(session.get(Book, id_)).dict()
    for key in book_data.keys():
        assert created_book.get(key) == book_data.get(key)
    assert created_book.get("id") == id_


def test_read_book(client: TestClient, stored_book: Dict[str, Any]) -> None:
    id_ = stored_book.get("id")

    response = client.get(f"/book/{id_}")  # act

    retrieved_book = response.json()
    assert response.status_code == 200
    for key in retrieved_book.keys():
        assert retrieved_book.get(key) == stored_book.get(key)


def test_update_book(client: TestClient, stored_book: Dict[str, Any]) -> None:
    id_ = stored_book.get("id")
    book_data = {
        "title": "Book 3",
        "description": "True Detective",
        "pages": 350,
    }

    response = client.put(f"/book/{id_}", json=book_data)  # act

    assert response.status_code == 200
    updated_book = response.json()
    for key in book_data.keys():
        assert book_data.get(key) == updated_book.get(key)
        assert stored_book.get(key) != updated_book.get(key)
    assert updated_book.get("id") == stored_book.get("id")


def test_delete_book(
    client: TestClient, session: AsyncSession, stored_book: Dict[str, Any]
) -> None:
    id_ = stored_book.get("id")

    response = client.delete(f"/book/{id_}")  # act

    assert response.status_code == 204
    assert asyncio.run(session.get(Book, id_)) is None


if __name__ == "__main__":
    pytest.main()
