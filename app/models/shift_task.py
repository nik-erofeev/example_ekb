from datetime import date, datetime

from sqlalchemy import DateTime, false, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import models
from app.database import Base


class ShiftTask(Base, models.IdMixin):
    __tablename__ = "shift_tasks"

    status_closed: Mapped[bool] = mapped_column(
        default=False,
        server_default=false(),
        nullable=False,
    )
    task_shift: Mapped[str] = mapped_column(String(100), nullable=False)
    line: Mapped[str] = mapped_column(String(100), nullable=False)
    shift: Mapped[str] = mapped_column(String(100), nullable=False)
    brigade: Mapped[str] = mapped_column(String(100), nullable=False)
    batch_number: Mapped[int] = mapped_column(nullable=False, unique=True)
    batch_date: Mapped[date] = mapped_column(
        nullable=False,
        unique=True
    )
    nomenclature: Mapped[str] = mapped_column(String(255), nullable=False)
    ecn_code: Mapped[str] = mapped_column(String(6), nullable=False)
    rc_identifier: Mapped[str] = mapped_column(String(10), nullable=False)

    date_started_shift: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    date_end_shift: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    closed_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
        default=None,
    )

    def close(self):
        self.closed_at = datetime.now()

    def open(self):
        self.closed_at = None
