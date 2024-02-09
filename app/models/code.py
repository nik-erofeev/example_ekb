from datetime import datetime

from sqlalchemy import false, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import models
from app.database import Base


class Code(Base, models.IdMixin):
    __tablename__ = "codes"

    unique_product_code: Mapped[str] = mapped_column(String(30), unique=True)
    is_aggregated: Mapped[bool] = mapped_column(
        default=False,
        server_default=false(),
        nullable=False,
    )
    aggregated_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
        default=None,
    )

    shift_task_id: Mapped[int] = mapped_column(ForeignKey("shift_tasks.id"))
    shift_task: Mapped["models.shift_task.ShiftTask"] = relationship(
        back_populates="codes",
    )
