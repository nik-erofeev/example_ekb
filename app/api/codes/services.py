from sqlalchemy.exc import IntegrityError

from app.api.codes.exceptions import http_code_conflict_exception
from app.api.codes.repository import CodeRepository
from app.api.codes.schemas import CodeBaseSchemas, CodeResponseSchemas
from app.api.common.services import BaseService
from app.api.shift_tasks.schemas import TaskByButchNumberRequest
from app.api.shift_tasks.utils import get_task_by_batch_number
from app.database import SessionDep


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
