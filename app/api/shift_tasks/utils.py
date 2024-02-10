from app.api.shift_tasks.repository import ShiftTaskRepository
from app.api.shift_tasks.schemas import TaskByButchNumberRequest
from app.database import SessionDep
from app.models import ShiftTask


async def get_task_by_batch_number(
    task_data: TaskByButchNumberRequest,
    session: SessionDep,
) -> ShiftTask | None:
    search_select = ShiftTaskRepository.search(
        batch_number=task_data.batch_number,
    )
    result = await session.execute(search_select)

    return result.scalar_one_or_none()
