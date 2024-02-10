from app.api.codes.repository import CodeRepository
from app.api.codes.schemas import CodeBaseSchemas, CodeResponseSchemas
from app.api.codes.utils import get_code
from app.api.common.services import BaseService
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

            shift_task = await get_task_by_batch_number(
                data.batch_number,
                session,
            )
            existing_code = await get_code(data.unique_product_code, session)

            if (shift_task is not None) and (existing_code is None):
                if (
                    shift_task.batch_number == data.batch_number
                    and shift_task.batch_date == data.batch_date
                ):

                    insert_code = cls.repository.insert(
                        obj_data={
                            "unique_product_code": data.unique_product_code,
                            "shift_task_id": shift_task.id,
                        },
                    )

                    result = await session.scalars(insert_code)
                    await session.flush()

                    list_code.append(result.one())

        return list_code
