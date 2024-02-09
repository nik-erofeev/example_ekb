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
    ShiftTaskUpdateSchemas,
)
from app.database import SessionDep
from app.models import ShiftTask


class ShiftTaskService(BaseService):
    repository = ShiftTaskRepository

    @classmethod
    async def create(
        cls,
        data_list: list[ShiftTaskCreateSchemas],
        session: SessionDep,
    ) -> list[ShiftTask]:

        list_task = []

        for data in data_list:

            if data.status_closed:
                data = data.model_dump(by_alias=True)
                data["closed_at"] = datetime.now()
            else:
                data = data.model_dump(by_alias=True)

            search_task = cls.repository.search(
                batch_number=data["batch_number"],
            )
            result_task = await session.execute(search_task)
            exist_task = result_task.scalar_one_or_none()

            if exist_task is None:
                try:
                    insert_shift_task = cls.repository.insert(data)
                    result = await session.scalars(insert_shift_task)
                    await session.flush()

                    list_task.append(result.one())
                except IntegrityError:
                    raise http_data_conflict_exception

            else:

                update_shift_task = cls.repository.update(exist_task.id, data)
                result = await session.scalars(update_shift_task)
                await session.flush()

                list_task.append(result.one())

        return list_task

    @classmethod
    async def get(
        cls,
        task_id: conint(gt=0),
        session: SessionDep,
    ) -> ShiftTask:
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
    ) -> list[ShiftTask]:

        return await super().get_many_query(
            session,
            pagination,
            query_params_task,
        )

    @classmethod
    async def edit(
        cls,
        task_id: int,
        data: ShiftTaskUpdateSchemas,
        session: SessionDep,
    ) -> ShiftTask:

        try:

            if data.status_closed is None:
                return await super().edit(task_id, data, session)

            else:
                update_data = data.model_dump(exclude_unset=True)
                if data.status_closed:
                    update_data["closed_at"] = datetime.now()
                else:
                    update_data["closed_at"] = None

                update_task = cls.repository.update(
                    task_id,
                    update_data,
                )

                result = await session.scalars(update_task)

                await session.flush()

                return result.one()

        except IntegrityError:
            raise http_data_conflict_exception

        except NoResultFound:
            raise http_not_found_exception
