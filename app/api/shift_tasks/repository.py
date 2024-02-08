from app.api.common.repository import BaseRepository, BaseSearchMixin
from app.models import ShiftTask


class ShiftTaskRepository(BaseRepository, BaseSearchMixin):
    model = ShiftTask
