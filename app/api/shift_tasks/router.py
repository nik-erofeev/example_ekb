from fastapi import APIRouter, status

from app.api.shift_tasks.schemas import ShiftTaskResponseSchemas
from app.api.shift_tasks.services import ShiftTaskService


router = APIRouter(
    prefix="/shift_tasks",
    tags=["Сменный задания"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ShiftTaskResponseSchemas,
)
async def create_shift_tasks(task: ShiftTaskService.create_dep):
    return task


@router.get(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=ShiftTaskResponseSchemas,
)
async def get_shift_tasks_by_id(task_id: ShiftTaskService.get_dep):
    return task_id


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[ShiftTaskResponseSchemas],
)
async def get_many_shift_tasks(task: ShiftTaskService.get_many_query_dep):
    return task


@router.patch(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=ShiftTaskResponseSchemas,
)
async def edit_task(task: ShiftTaskService.edit_dep):
    return task
