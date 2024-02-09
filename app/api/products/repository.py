from app.api.common.repository import BaseRepository
from app.models import Code


class CodeRepository(BaseRepository):
    model = Code
