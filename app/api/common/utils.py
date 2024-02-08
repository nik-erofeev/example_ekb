from typing import Annotated

import sqlalchemy
from fastapi import Depends, params, Response
from fastapi.requests import Request
from sqlalchemy import func

from app.api.common.schemas import PaginationParams
from app.database import Base, SessionDep


def paginate_select(select: sqlalchemy.Select, pagination: PaginationParams):
    offset = (pagination.page - 1) * pagination.per_page
    return select.offset(offset).limit(pagination.per_page)


def set_pagination_headers(model: type[Base]) -> params.Depends:
    async def _get_headers(
        pagination: Annotated[PaginationParams, Depends()],
        request: Request,
        response: Response,
        session: SessionDep,
    ):
        rows_num_select = await session.scalar(func.count(model.id))
        total_pages = rows_num_select // pagination.per_page + bool(
            rows_num_select % pagination.per_page,
        )

        paginator = {}

        if total_pages == 0:
            return None

        if pagination.page != 1:
            paginator["first"] = request.url.remove_query_params("page")

        if pagination.page != total_pages:
            paginator["last"] = request.url.include_query_params(
                page=total_pages,
            )

        if pagination.page + 1 <= total_pages:
            paginator["next"] = request.url.include_query_params(
                page=pagination.page + 1,
            )

        if pagination.page - 1 >= 1:
            paginator["prev"] = request.url.include_query_params(
                page=pagination.page - 1,
            )

        link_header = ", ".join(
            f'<{url}>; rel="{rel}"' for rel, url in paginator.items()
        )

        response.headers["Link"] = link_header

    return Depends(_get_headers)


PaginationDep = Annotated[PaginationParams, Depends()]
