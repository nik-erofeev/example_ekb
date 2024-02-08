from abc import ABC, abstractmethod

from pydantic import BaseModel

from app.api.common.repository import BaseRepository
from app.api.common.utils import paginate_select, PaginationDep
from app.database import SessionDep


class AbstractBaseService(ABC):
    repository: type[BaseRepository]

    @classmethod
    @abstractmethod
    async def create(cls, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    async def get(cls, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    async def get_many(cls, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    async def get_many_query(cls, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    async def edit(cls, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    async def delete(cls, *args, **kwargs):
        pass


class BaseService(AbstractBaseService):
    repository: type[BaseRepository]

    @classmethod
    async def _create(cls, data: BaseModel, session: SessionDep):
        data = data.model_dump(by_alias=True)
        insert = cls.repository.insert(data)

        result = await session.scalars(insert)
        await session.flush()

        return result.one()

    @classmethod
    async def _get(cls, obj_id: int, session: SessionDep):
        select = cls.repository.select(obj_id)

        result = await session.scalars(select)

        return result.one()

    @classmethod
    async def _get_many(cls, pagination: PaginationDep, session: SessionDep):
        select = cls.repository.select_many()
        paginated = paginate_select(select, pagination)

        result = await session.scalars(paginated)

        return result.all()

    @classmethod
    async def _get_many_query(
        cls,
        session: SessionDep,
        pagination: PaginationDep | None = None,
        query_params=None,
    ):
        if query_params:
            query_params = query_params.model_dump(
                by_alias=True,
                exclude_defaults=True,
            )

        select = cls.repository.select_many(query_params)
        if pagination:
            select = paginate_select(select, pagination)

        result = await session.scalars(select)
        return result.all()

    @classmethod
    async def _edit(cls, obj_id: int, data: BaseModel, session: SessionDep):
        update = cls.repository.update(
            obj_id,
            data.model_dump(by_alias=True, exclude_unset=True),
        )

        result = await session.scalars(update)

        await session.flush()

        return result.one()

    @classmethod
    async def _delete(cls, obj_id: int, session: SessionDep):
        delete = cls.repository.delete(obj_id)

        result = await session.scalars(delete)

        await session.flush()

        return result.one()

    @classmethod
    async def create(cls, *args, **kwargs):
        return await cls._create(*args, **kwargs)

    @classmethod
    async def get(cls, *args, **kwargs):
        return await cls._get(*args, **kwargs)

    @classmethod
    async def get_many(cls, *args, **kwargs):
        return await cls._get_many(*args, **kwargs)

    @classmethod
    async def get_many_query(cls, *args, **kwargs):
        return await cls._get_many_query(*args, **kwargs)

    @classmethod
    async def edit(cls, *args, **kwargs):
        return await cls._edit(*args, **kwargs)

    @classmethod
    async def delete(cls, *args, **kwargs):
        return await cls._delete(*args, **kwargs)
