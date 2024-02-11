from datetime import datetime

from fastapi import HTTPException, status

from app.api.codes.exceptions import http_not_found_code_exception
from app.api.codes.repository import CodeRepository
from app.api.codes.schemas import (
    CodeBaseSchemas,
    CodeResponseSchemas,
    UniqueCodeSchemas,
)
from app.api.codes.utils import get_code
from app.api.common.services import BaseService
from app.api.shift_tasks.utils import get_task_by_batch_number
from app.database import SessionDep
from app.models import Code


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
                    shift_task.batch_number == data.batch_number  # noqa
                    and shift_task.batch_date == data.batch_date  # noqa
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

    @classmethod
    async def aggregate_codes(
        cls,
        task_id: int,
        data: UniqueCodeSchemas,
        session: SessionDep,
    ) -> Code:

        existing_code = await get_code(data.unique_product_code, session)
        if existing_code is None:
            raise http_not_found_code_exception

        if (
            existing_code.shift_task_id == task_id
        ) and not existing_code.is_aggregated:
            existing_code.is_aggregated = True
            existing_code.aggregated_at = datetime.now()

            return existing_code

        if existing_code.is_aggregated:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"unique code already used at {existing_code.aggregated_at}",  # noqa
            )

        if existing_code is not None and existing_code.shift_task_id != task_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="unique code is attached to another batch",
            )

    @classmethod
    @property
    def aggregate_codes_dep(cls):
        return cls._dep_get(cls.aggregate_codes)
