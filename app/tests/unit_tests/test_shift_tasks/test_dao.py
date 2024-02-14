import pytest

from app.api.shift_tasks.schemas import ShiftTaskCreateSchemas
from app.api.shift_tasks.services import ShiftTaskService


# @pytest.mark.asyncio
# async def test_get_shift_task(session_fake):
#
#     # Предположим, у вас есть переменная task_id, которую вы хотите использовать для теста   # noqa
#     task_id = 12345
#     # Вызываем метод get() сервиса ShiftTaskService
#     retrieved_task = await ShiftTaskService.get(task_id, session=session_fake)
#
#     # Проверяем, что полученная задача не является None
#     assert retrieved_task is not None



@pytest.mark.asyncio
async def test_create_shift_tasks(session_fake):
    # Создаем список данных для создания задач
    data_list_2 = [
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

    data_list = [ShiftTaskCreateSchemas(**item) for item in data_list_2]

    # Вызываем метод create из ShiftTaskService с передачей session_mock
    new_tasks = await ShiftTaskService.create(data_list, session_fake)

    # Проверяем, что метод create возвращает список задач
    assert isinstance(new_tasks, list)
