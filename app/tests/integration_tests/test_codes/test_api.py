



async def test_create_unique_codes(ac):

    response = await ac.post(
        "/api/v1/codes/",
        json=[
            {
                "УникальныйКодПродукта": "12gRV60MMsn1",
                "НомерПартии": 22222,
                "ДатаПартии": "2024-01-30",
            },
            {
                "УникальныйКодПродукта": "12gRV60MMsn2",
                "НомерПартии": 22223,
                "ДатаПартии": "2024-03-30",
            },
        ],
    )

    assert response.status_code == 201
