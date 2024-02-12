from httpx import AsyncClient


async def test_create_shift_tasks(ac: AsyncClient):

    response = await ac.post(
        "/api/v1/shift_tasks/",
        json=[
            {
                "СтатусЗакрытия": False,
                "ПредставлениеЗаданияНаСмену": "Задание на смену 2345",
                "Линия": "Т2",
                "Смена": "1",
                "Бригада": "Бригада №4",
                "НомерПартии": 22222,
                "ДатаПартии": "2024-01-30",
                "Номенклатура": "Какая то номенклатура",
                "КодЕКН": "456678",
                "ИдентификаторРЦ": "A",
                "ДатаВремяНачалаСмены": "2024-01-30T20:00:00+05:00",
                "ДатаВремяОкончанияСмены": "2024-01-31T08:00:00+05:00",
            },
            {
                "СтатусЗакрытия": False,
                "ПредставлениеЗаданияНаСмену": "Задание на смену 3",
                "Линия": "Т3",
                "Смена": "2",
                "Бригада": "Бригада №2",
                "НомерПартии": 22223,
                "ДатаПартии": "2024-03-30",
                "Номенклатура": "Какая то номенклатур3",
                "КодЕКН": "456673",
                "ИдентификаторРЦ": "Б",
                "ДатаВремяНачалаСмены": "2024-03-30T20:00:00+05:00",
                "ДатаВремяОкончанияСмены": "2024-03-31T08:00:00+05:00",
            },
            {
                "СтатусЗакрытия": True,
                "ПредставлениеЗаданияНаСмену": "Задание на смену 99",
                "Линия": "Т99",
                "Смена": "10",
                "Бригада": "Бригада №22",
                "НомерПартии": 22227,
                "ДатаПартии": "2024-05-30",
                "Номенклатура": "Какая то номенклатур5",
                "КодЕКН": "456679",
                "ИдентификаторРЦ": "Пп",
                "ДатаВремяНачалаСмены": "2024-05-30T20:00:00+05:00",
                "ДатаВремяОкончанияСмены": "2024-05-31T08:00:00+05:00",
            },
        ],
    )

    assert response.status_code == 201


