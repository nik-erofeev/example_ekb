from app.api.shift_tasks.repository import ShiftTaskRepository
from app.database import SessionDep
from app.models import ShiftTask


async def get_task_by_batch_number(
    number: int,
    session: SessionDep,
) -> ShiftTask | None:
    search_select = ShiftTaskRepository.search(
        batch_number=number,
    )
    result = await session.execute(search_select)

    return result.scalar_one_or_none()
