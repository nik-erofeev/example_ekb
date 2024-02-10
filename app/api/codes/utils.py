from app.api.codes.repository import CodeRepository
from app.database import SessionDep
from app.models import Code


async def get_code(
    code: str,
    session: SessionDep,
) -> Code | None:
    search_select = CodeRepository.search(
        unique_product_code=code,
    )
    result = await session.execute(search_select)

    return result.scalar_one_or_none()
