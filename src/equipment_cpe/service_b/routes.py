from typing import Any

from celery.result import AsyncResult
from fastapi import APIRouter

from equipment_cpe.celery_app import celery_app
from equipment_cpe.service_b.models import (
    SetCpeRequest,
    TaskIdResponse,
    TaskStatusResponse,
)
from equipment_cpe.service_b.tasks import task_set_async_cpe

router = APIRouter(prefix="/equipment")


@router.post("/cpe/{equipment_id}/task/{task_id}")
async def get_result_set_cpe_task(
    equipment_id: str,
    task_id: str,
) -> TaskStatusResponse:
    result: AsyncResult[dict[str, Any]] = AsyncResult(task_id, app=celery_app)
    if result.successful():
        result_data: dict[str, Any] = result.get()
        code = result_data.get("code", 500)
        result_message = result_data.get("message", "Error")

        completed_code = 200
        if code == completed_code:
            message = "Completed"
        else:
            message = result_message
        return TaskStatusResponse(code=200, message=message)

    if result.status in ("PENDING", "STARTED", "RETRY"):
        return TaskStatusResponse(code=204, message="Task is still running")

    return TaskStatusResponse(code=500, message=result.status)


@router.post("/cpe/{equipment_id}/task")
async def set_cpe_task(
    equipment_id: str, set_cpe_request: SetCpeRequest
) -> TaskIdResponse:
    task = task_set_async_cpe.delay(equipment_id, set_cpe_request.model_dump())
    return TaskIdResponse(code=200, taskId=task.id)
