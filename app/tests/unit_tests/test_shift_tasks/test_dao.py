import pytest
from fastapi import HTTPException

from app.api.shift_tasks.schemas import (
    ShiftTaskCreateSchemas,
    ShiftTaskUpdateSchemas,
)
from app.api.shift_tasks.services import ShiftTaskService


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "task_id, brigade, is_present",
    [
        (1, "Бригада №1", True),
        (2, "Бригада №2", True),
        (99, ".........", False),
    ],
)
async def test_get_shift_task(session_fake, task_id, brigade, is_present):

    if is_present:
        task = await ShiftTaskService.get(task_id, session=session_fake)
        assert task.brigade == brigade
    else:
        with pytest.raises(HTTPException) as exc:
            await ShiftTaskService.get(task_id, session=session_fake)
            assert exc.value.status_code == 404
            assert exc.value.detail == "Сменное задание не найдено"


@pytest.mark.asyncio
async def test_create_shift_tasks(session_fake):
    # Создаем список данных для создания задач
    list_task_input = [
        {
            "СтатусЗакрытия": False,
            "ПредставлениеЗаданияНаСмену": "Задание на смену 2345",
            "Линия": "Т2",
            "Смена": "1",
            "Бригада": "Бригада №4",
            "НомерПартии": 11111111,
            "ДатаПартии": "2027-01-30",
            "Номенклатура": "Какая то номенклатура",
            "КодЕКН": "456678",
            "ИдентификаторРЦ": "A",
            "ДатаВремяНачалаСмены": "2024-01-30T20:00:00+05:00",
            "ДатаВремяОкончанияСмены": "2024-01-31T08:00:00+05:00",
        },
    ]

    tasks_data = [ShiftTaskCreateSchemas(**item) for item in list_task_input]
    result_tasks = await ShiftTaskService.create(tasks_data, session_fake)

    assert isinstance(result_tasks, list)

    for task in result_tasks:
        assert task.brigade == "Бригада №4"


@pytest.mark.parametrize(
    "task_shift, line, status_closed, id_task, is_present",
    [
        ("Обновленное задание", "Обновленная линия", True, 1, True),
        ("", "", True, 99, False),
    ],
)
@pytest.mark.asyncio
async def test_edit(
    task_shift,
    line,
    status_closed,
    id_task,
    is_present,
    session_fake,
):

    updated_task_data = {
        "task_shift": task_shift,
        "line": line,
        "status_closed": status_closed,
    }
    updated_task_model = ShiftTaskUpdateSchemas(**updated_task_data)
    if is_present:

        update_task = await ShiftTaskService.edit(
            id_task,
            updated_task_model,
            session_fake,
        )
        assert update_task.task_shift == updated_task_data["task_shift"]
        assert update_task.line == updated_task_data["line"]

    else:
        with pytest.raises(HTTPException) as exc:
            await ShiftTaskService.edit(
                id_task,
                updated_task_model,
                session_fake,
            )
            assert exc.value.status_code == 404
            assert exc.value.detail == "Сменное задание не найдено"
