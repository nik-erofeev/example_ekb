"""Слой работы бд"""

from abc import ABC
from collections.abc import Mapping

import sqlalchemy

from app.database import Base


class BaseSearchMixin(ABC):
    model: type[Base]

    @classmethod
    def search(cls, **kwargs) -> sqlalchemy.Select:
        """Возвращает селект для одного результата поиска по полям."""

        select = sqlalchemy.select(cls.model).filter_by(**kwargs)

        if hasattr(cls.model, "is_deleted"):
            return select.filter_by(is_deleted=False)

        return select


class BaseRepository:
    model: type[Base]

    @classmethod
    def select(cls, obj_id: int) -> sqlalchemy.Select:
        """Возвращает селект для одного результата по айди."""

        select = sqlalchemy.select(cls.model).filter_by(id=obj_id)
        return select

    @classmethod
    def select_many(
        cls,
        obj_filter: Mapping | None = None,
    ) -> sqlalchemy.Select:
        """Возвращает селект для множества результатов по фильтру."""
        select = sqlalchemy.select(cls.model)

        if obj_filter is None:
            return select

        return select.filter_by(**obj_filter)

    @classmethod
    def insert(cls, obj_data: Mapping, **extra_fields) -> sqlalchemy.Insert:
        """Возвращает инсерт для одного элемента."""

        return (
            sqlalchemy.insert(cls.model)
            .values(**obj_data, **extra_fields)
            .returning(
                cls.model,
            )
        )

    @classmethod
    def delete(cls, obj_id: int) -> sqlalchemy.Delete | sqlalchemy.Update:
        """
        Возвращает делит для одного элемента.
        """

        return (
            sqlalchemy.delete(cls.model)
            .filter_by(id=obj_id)
            .returning(
                cls.model,
            )
        )

    @classmethod
    def update(
        cls,
        obj_id: int,
        update_fields: Mapping,
        **extra_fields,
    ) -> sqlalchemy.Update:
        """Возвращает апдейт для элементов по айди."""

        return (
            sqlalchemy.update(cls.model)
            .filter_by(id=obj_id)
            .values(**update_fields, **extra_fields)
            .returning(cls.model)
        )
