from datetime import date, datetime

from pydantic import BaseModel, Field

from app.api.codes.schemas import CodeResponseSchemas


class ShiftTaskBaseSchemas(BaseModel):
    status_closed: bool = Field(..., validation_alias="СтатусЗакрытия")
    task_shift: str = Field(..., validation_alias="ПредставлениеЗаданияНаСмену")
    line: str = Field(..., validation_alias="Линия")
    shift: str = Field(..., validation_alias="Смена")
    brigade: str = Field(..., validation_alias="Бригада")
    batch_number: int = Field(..., validation_alias="НомерПартии")
    batch_date: date = Field(..., validation_alias="ДатаПартии")
    nomenclature: str = Field(..., validation_alias="Номенклатура")
    ecn_code: str = Field(..., validation_alias="КодЕКН")
    rc_identifier: str = Field(..., validation_alias="ИдентификаторРЦ")
    date_started_shift: datetime = Field(
        ...,
        validation_alias="ДатаВремяНачалаСмены",
    )
    date_end_shift: datetime = Field(
        ...,
        validation_alias="ДатаВремяОкончанияСмены",
    )


class ShiftTaskCreateSchemas(ShiftTaskBaseSchemas):
    pass


class ShiftTaskResponseSchemas(BaseModel):
    id: int
    status_closed: bool
    task_shift: str
    line: str
    shift: str
    brigade: str
    batch_number: int
    batch_date: date
    nomenclature: str
    ecn_code: str
    rc_identifier: str
    date_started_shift: datetime
    date_end_shift: datetime

    closed_at: datetime | None


class TaskWithCodesResponseSchemas(ShiftTaskResponseSchemas):
    codes: list[CodeResponseSchemas]


class ShiftTaskQueryParams(BaseModel):
    status_closed: bool | None = None
    batch_number: int | None = None
    batch_date: date | None = None
    nomenclature: str | None = None
    ecn_code: str | None = None
    rc_identifier: str | None = None


class ShiftTaskUpdateSchemas(BaseModel):
    status_closed: bool | None = None
    task_shift: str | None = None
    line: str | None = None
    shift: str | None = None
    brigade: str | None = None
    batch_number: int | None = None
    batch_date: date | None = None
    nomenclature: str | None = None
    ecn_code: str | None = None
    rc_identifier: str | None = None
    date_started_shift: datetime | None = None
    date_end_shift: datetime | None = None
