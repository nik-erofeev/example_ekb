from httpx import AsyncClient
import pytest


@pytest.mark.parametrize(
    "status_closed,task_shift,line,shift,brigade,batch_number,batch_date,nomenclature,ecn_code,rc_identifier,date_started_shift,date_end_shift,status_code",
    [
        (
            False,
            "ТЕСТЫ Задание на смену 2",
            "ТЕСТЫ ЛИНИЯ Т2",
            "ТЕСТЫ Смена 2",
            "ТЕСТЫ Бригада №2",
            22222,
            "2024-01-30",
            "ТЕСТЫ Какая то номенклатура2",
            "456678",
            "ТЕСТЫ A2",
            "2024-01-30T20:00:00+05:00",
            "2024-01-31T08:00:00+05:00",
            201,
        ),
        (
            False,
            "ТЕСТЫ Задание на смену 99",
            "ТЕСТЫ ЛИНИЯ Т99",
            "ТЕСТЫ Смена 99",
            "ТЕСТЫ Бригада №22",
            88888,
            "2024-01-30",
            "ТЕСТЫ Какая то номенклатур99",
            "456679",
            "ТЕСТЫ 99",
            "2024-05-30T20:00:00+05:00",
            "2024-05-31T08:00:00+05:00",
            409,
        ),
        (
            "dasd",
            "dasd",
            "dasd",
            "dasd",
            "dasd",
            "dasd",
            "dasd",
            "dasd",
            "dasd",
            "dasd",
            "dasd",
            "dasd",
            422,
        ),
    ],
)
async def test_create_shift_tasks(
    status_closed,
    task_shift,
    line,
    shift,
    brigade,
    batch_number,
    batch_date,
    nomenclature,
    ecn_code,
    rc_identifier,
    date_started_shift,
    date_end_shift,
    status_code,
    ac: AsyncClient,
):

    data = [
        {
            "СтатусЗакрытия": status_closed,
            "ПредставлениеЗаданияНаСмену": task_shift,
            "Линия": line,
            "Смена": shift,
            "Бригада": brigade,
            "НомерПартии": batch_number,
            "ДатаПартии": batch_date,
            "Номенклатура": nomenclature,
            "КодЕКН": ecn_code,
            "ИдентификаторРЦ": rc_identifier,
            "ДатаВремяНачалаСмены": date_started_shift,
            "ДатаВремяОкончанияСмены": date_end_shift,
        }
    ]

    response = await ac.post("/api/v1/shift_tasks/", json=data)

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "task_id,status_code",
    [
        (1, 200),
        (99, 404),
    ],
)
async def test_get_by_id(
    task_id,
    status_code,
    ac: AsyncClient,
):
    response = await ac.get(f"/api/v1/shift_tasks/{task_id}")
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "task_id, batch_date, status_code,",
    [
        (1, "2024-03-03", 409),
        (99, "2024-03-03", 404),
        (99, "", 422),
        (99, None, 409),
    ],
)
async def test_edit_task(
    task_id,
    batch_date,
    status_code,
    ac: AsyncClient,
):
    json_data = {} if batch_date is None else {"batch_date": batch_date}
    response = await ac.patch(f"api/v1/shift_tasks/{task_id}", json=json_data)
    assert response.status_code == status_code
