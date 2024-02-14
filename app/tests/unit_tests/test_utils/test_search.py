import pytest

from app.api.codes.utils import get_code
from app.api.shift_tasks.utils import get_task_by_batch_number


@pytest.mark.parametrize(
    "batch_number, id, is_present",
    [
        (22221, 1, True),
        (22222, 2, True),
        (555, "", False),
    ],
)
@pytest.mark.asyncio
async def test_get_task_by_batch_number(
    batch_number,
    id,
    is_present,
    session_fake,
):

    batch_number = await get_task_by_batch_number(
        number=batch_number,
        session=session_fake,
    )

    if is_present:
        assert batch_number.id == id
    else:
        assert batch_number is None


@pytest.mark.parametrize(
    "code, shift_task_id, is_present",
    [
        ("uniquecode1", 1, True),
        ("not_code", "", False),
    ],
)
@pytest.mark.asyncio
async def test_get_code(code, shift_task_id, is_present, session_fake):

    code = await get_code(code=code, session=session_fake)

    if is_present:
        assert code.shift_task_id == shift_task_id

    else:
        assert code is None
