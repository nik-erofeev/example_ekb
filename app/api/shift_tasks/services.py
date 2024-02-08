from datetime import datetime

from fastapi import Depends
from pydantic import conint
from sqlalchemy.exc import IntegrityError, NoResultFound

from app.api.common.services import BaseService
from app.api.common.utils import PaginationDep
from app.api.shift_tasks.exceptions import (
    http_data_conflict_exception,
    http_not_found_exception,
)
from app.api.shift_tasks.repository import ShiftTaskRepository
from app.api.shift_tasks.schemas import (
    ShiftTaskCreateSchemas,
    ShiftTaskQueryParams,
)
from app.database import SessionDep
from app.models import ShiftTask


class ShiftTaskService(BaseService):
    repository = ShiftTaskRepository

    @classmethod
    async def create(
        cls,
        data: ShiftTaskCreateSchemas,
        session: SessionDep,
    ) -> ShiftTask:

        if data.status_closed:
            data = data.model_dump(by_alias=True)
            data["closed_at"] = datetime.now()
        else:
            data = data.model_dump(by_alias=True)

        insert = cls.repository.insert(data)

        try:
            result = await session.scalars(insert)
            await session.flush()

        except IntegrityError:
            raise http_data_conflict_exception

        return result.one()

    @classmethod
    async def get(cls, task_id: conint(gt=0), session: SessionDep) -> ShiftTask:
        try:
            return await super().get(task_id, session)

        except NoResultFound:
            raise http_not_found_exception

    @classmethod
    async def get_many_query(
        cls,
        session: SessionDep,
        pagination: PaginationDep,
        query_params_task: ShiftTaskQueryParams = Depends(ShiftTaskQueryParams),
    ):
        return await super().get_many_query(
            session,
            pagination,
            query_params_task,
        )
