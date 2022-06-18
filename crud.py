from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import update, delete
from models import BookIn, Book


async def create_book(book: BookIn, session: AsyncSession):
    book = Book(**book.dict())
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return book


async def read_book(book_id: int, session: AsyncSession):
    book = await session.get(Book, book_id)
    return book


async def update_book(book_id: int, book: BookIn, session: AsyncSession):
    query = update(Book).where(Book.id == book_id).values(**book.dict())
    await session.execute(query)
    await session.commit()
    return await read_book(book_id, session)


async def delete_book(book_id: int, session: AsyncSession):
    query = delete(Book).where(Book.id == book_id)
    await session.execute(query)
    await session.commit()
