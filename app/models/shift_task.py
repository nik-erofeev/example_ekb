from datetime import date, datetime

from sqlalchemy import false, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import now

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
    line: Mapped[str] = mapped_column(String(10), nullable=False)
    shift: Mapped[str] = mapped_column(String(32), nullable=False)
    brigade: Mapped[str] = mapped_column(String(20), nullable=False)
    batch_number: Mapped[int] = mapped_column(nullable=False, unique=True)
    batch_date: Mapped[date] = mapped_column(unique=True)
    nomenclature: Mapped[str] = mapped_column(String(20), nullable=False)
    ecn_code: Mapped[str] = mapped_column(String(6), nullable=False)
    rc_identifier: Mapped[str] = mapped_column(String(10), nullable=False)
    date_started_shift: Mapped[datetime] = mapped_column(server_default=now())
    date_end_shift: Mapped[datetime]

    closed_at: Mapped[datetime | None]

    def close(self):
        if not self.status_closed:
            self.status_closed = True
            self.closed_at = datetime.now()
