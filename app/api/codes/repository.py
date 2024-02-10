from app.api.common.repository import BaseRepository, BaseSearchMixin
from app.models import Code


class CodeRepository(BaseRepository, BaseSearchMixin):
    model = Code
