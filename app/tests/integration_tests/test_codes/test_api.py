from httpx import AsyncClient
import pytest


@pytest.mark.parametrize(
    "batch_number,batch_date,unique_product_code,status_code",
    [
        (22222, "2024-01-30", "тест_код1", 201),
        (22222, "2024-01-30", "тест_код2", 201),
        ("aaa", "aaa", "aaa", 422),
    ],
)
async def test_create_unique_codes(
    batch_number,
    batch_date,
    unique_product_code,
    status_code,
    ac: AsyncClient,
):
    data = [
        {
            "НомерПартии": batch_number,
            "ДатаПартии": batch_date,
            "УникальныйКодПродукта": unique_product_code,
        }
    ]
    response = await ac.post("/api/v1/codes/", json=data)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "task_id,unique_product_code,status_code",
    [
        (1, "uniquecode1", 200),
        (4, "uniquecode4", 400),
        (2, "uniquecode111", 400),
        (2, "asd", 404),
        ("", "", 422),
    ],
)
async def test_aggregated(
    task_id,
    unique_product_code,
    status_code,
    ac: AsyncClient,
):
    response = await ac.patch(
        f"/api/v1/codes/?task_id={task_id}",
        json={"task_id": task_id, "unique_product_code": unique_product_code},
    )
    assert response.status_code == status_code
