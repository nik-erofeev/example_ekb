"""Модуль работы с Базой Данных"""

import contextlib
from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, declared_attr

from app.config import settings


if settings.MODE == "TEST":
    DATABASE_URL = settings.database_url_test
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.database_url
    DATABASE_PARAMS = {}

engine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
    **DATABASE_PARAMS,
)


async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Базовая модель"""

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    def __repr__(self):
        """
        Печать орм-объектов с отображением атрибутов
        """

        fmt = "{}.{}({})"
        package = self.__class__.__module__
        class_ = self.__class__.__name__
        attrs = sorted(
            (k, getattr(self, k)) for k in self.__mapper__.columns.keys()
        )
        sattrs = ", ".join("{}={!r}".format(*x) for x in attrs)
        return fmt.format(package, class_, sattrs)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Генератор, который возвращает сессию подключения к БД
    :return: AsyncSession
    """
    async with async_session() as session:  # type: AsyncSession
        try:
            yield session
        except Exception as exc:
            await session.rollback()
            raise exc
        else:
            await session.commit()


session_context_manager = contextlib.asynccontextmanager(get_session)

SessionDep = Annotated[AsyncSession, Depends(get_session)]
