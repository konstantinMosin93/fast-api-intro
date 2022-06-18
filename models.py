import datetime

import sqlalchemy
from sqlmodel import SQLModel, Field, Column, DateTime


class BookBase(SQLModel):
    title: str
    description: str | None = None
    pages: int


class BookIn(BookBase):
    pass


class BookOut(BookBase):
    id: int
    created_at: datetime.datetime
    last_modified_at: datetime.datetime


class Book(BookBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime.datetime = Field(
        sa_column=Column(
            DateTime,
            server_default=sqlalchemy.func.now(),
            nullable=False
        )
    )
    last_modified_at: datetime.datetime = Field(
        sa_column=Column(
            DateTime,
            server_default=sqlalchemy.func.now(),
            onupdate=sqlalchemy.func.now(),
            nullable=False
        )
    )
