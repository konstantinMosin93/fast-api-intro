from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

import src.crud as crud
from src.db import get_session
from src.models import BookIn
from src.models import BookOut


router = APIRouter(
    prefix="/book",
    tags=["books"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/",
    response_model=BookOut,
    response_model_exclude={"last_modified_at"},
    status_code=201,
    summary="Create Book",
    response_description="The created book",
)
async def create_book(
    book: BookIn, session: AsyncSession = Depends(get_session)
):
    """
    Create a book with all the information:
    - **title**: each book must have a title
    - **description**: each book can have a description (not required)
    - **pages**: each book must have number of pages
    """
    return await crud.create_book(book, session)


@router.get(
    "/{book_id}",
    response_model=BookOut,
    summary="Read Book",
    description="To read all book information you should pass book id.",
)
async def read_book(
    book_id: int, session: AsyncSession = Depends(get_session)
):
    return await crud.read_book(book_id, session)


@router.put(
    "/{book_id}",
    response_model=BookOut,
    summary="Update Book",
)
async def update_book(
    book_id: int, book: BookIn, session: AsyncSession = Depends(get_session)
):
    """
    Update a one or more than one book fields:
    - **title**: a new book title
    - **description**: a new book description
    - **pages**: a new number of pages
    """
    return await crud.update_book(book_id, book, session)


@router.delete(
    "/{book_id}",
    summary="Delete book",
    description="To delete book you should pass book id.",
)
async def delete_book(
    book_id: int, session: AsyncSession = Depends(get_session)
) -> Response:
    await crud.delete_book(book_id, session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
