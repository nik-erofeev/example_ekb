from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from app.api.codes.exceptions import http_code_conflict_exception
from app.api.codes.repository import CodeRepository
from app.api.codes.schemas import CodeBaseSchemas, CodeResponseSchemas
from app.api.common.services import BaseService
from app.api.shift_tasks.repository import ShiftTaskRepository
from app.database import SessionDep
from app.models import ShiftTask


class TaskByButchNumberRequest(BaseModel):
    batch_number: int


async def get_task_by_batch_number(
    task_data: TaskByButchNumberRequest,
    session: SessionDep,
) -> ShiftTask | None:
    search_select = ShiftTaskRepository.search(
        batch_number=task_data.batch_number,
    )
    result = await session.execute(search_select)

    return result.scalar_one_or_none()


class CodeService(BaseService):
    repository = CodeRepository

    @classmethod
    async def create(
        cls,
        data_list: list[CodeBaseSchemas],
        session: SessionDep,
    ) -> list[CodeResponseSchemas]:

        list_code = []

        for data in data_list:

            task_data = TaskByButchNumberRequest(batch_number=data.batch_number)
            shift_task = await get_task_by_batch_number(task_data, session)

            if shift_task is not None:
                if (
                    shift_task.batch_number == data.batch_number
                    and shift_task.batch_date == data.batch_date
                ):
                    try:

                        insert_code = cls.repository.insert(
                            obj_data={
                                "unique_product_code": data.unique_product_code,
                                "shift_task_id": shift_task.id,
                            },
                        )

                        result = await session.scalars(insert_code)
                        await session.flush()

                        list_code.append(result.one())
                    except IntegrityError:
                        raise http_code_conflict_exception

        return list_code
