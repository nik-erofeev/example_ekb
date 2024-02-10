from datetime import date, datetime

from pydantic import BaseModel, Field


class CodeBaseSchemas(BaseModel):
    batch_number: int = Field(..., validation_alias="НомерПартии")
    batch_date: date = Field(..., validation_alias="ДатаПартии")
    unique_product_code: str = Field(
        ...,
        validation_alias="УникальныйКодПродукта",
    )


class CodeCreateSchemas(CodeBaseSchemas):
    pass


class CodeResponseSchemas(BaseModel):
    id: int
    unique_product_code: str
    shift_task_id: int
    is_aggregated: bool
    aggregated_at: datetime | None


class UniqueCodeSchemas(BaseModel):
    unique_product_code: str
