import pytest
from fastapi import HTTPException

from app.api.codes.schemas import CodeBaseSchemas, UniqueCodeSchemas
from app.api.codes.services import CodeService


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "batch_number, batch_date, unique_product_code, is_present",
    [
        (22221, "2024-01-01", "тест код1", True),
        (1, "2024-01-01", "тест код1", False),
    ],
)
async def test_create(
    session_fake,
    batch_number,
    batch_date,
    unique_product_code,
    is_present,
):

    codes_input = {
        "НомерПартии": batch_number,
        "ДатаПартии": batch_date,
        "УникальныйКодПродукта": unique_product_code,
    }

    codes_data = CodeBaseSchemas(**codes_input)
    codes_result = await CodeService.create([codes_data], session_fake)
    assert isinstance(codes_result, list)

    if is_present:
        assert len(codes_result) == 1
    else:
        assert len(codes_result) == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "task_id, unique_product_code,is_aggregated, is_present,",
    [
        (1, "uniquecode11", False, True),  # существует - не использован
        (1, "uniquecode1", True, True),  # существует - использован
        (1, "not_cod", True, False),  # не существует кода
        (2, "uniquecode11", False, True),  # существует - но другая партия !!!!!
    ],
)
async def test_aggregate_codes(
    task_id,
    unique_product_code,
    is_aggregated,
    is_present,
    session_fake,
):

    code_data = UniqueCodeSchemas(unique_product_code=unique_product_code)

    # другая партия
    if task_id == 2:
        with pytest.raises(HTTPException) as exc:
            await CodeService.aggregate_codes(
                task_id=task_id,
                data=code_data,
                session=session_fake,
            )

        # fmt: off
        assert exc.value.status_code == 400
        assert exc.value.detail == "unique code is attached to another batch"
        # fmt: on

    # существует - не агрегирован
    elif is_present and not is_aggregated:

        code = await CodeService.aggregate_codes(
            task_id=task_id,
            data=code_data,
            session=session_fake,
        )
        # изменили агрегацию на True
        assert code.is_aggregated
        assert code.unique_product_code == unique_product_code

    # существует - агрегирован
    elif is_present and is_aggregated:
        with pytest.raises(HTTPException) as exc:
            await CodeService.aggregate_codes(
                task_id=task_id,
                data=code_data,
                session=session_fake,
            )

        assert exc.value.status_code == 400

    # не существует
    elif not is_present:
        with pytest.raises(HTTPException) as exc:
            await CodeService.aggregate_codes(
                task_id=task_id,
                data=code_data,
                session=session_fake,
            )

        # fmt: off
        assert exc.value.status_code == 404
        assert exc.value.detail == "Продукции с данным уникальным кодом не существует"  # noqa
        # fmt: on
