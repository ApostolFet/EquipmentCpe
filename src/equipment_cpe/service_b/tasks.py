from typing import Any

import httpx
from celery import Task

from equipment_cpe.celery_app import celery_app
from equipment_cpe.config import SeriveceAConfig


@celery_app.task(
    bind=True,
    retry_kwargs={"max_retries": 3},
    retry_backoff=True,
)
def task_set_async_cpe(
    task: "Task[[str, dict[str, Any]], dict[str, str | int]]",
    equipment_id: str,
    set_equipment_request: dict[str, Any],
) -> dict[str, str | int]:
    service_a_config = SeriveceAConfig.load_config()

    method_url = "/api/v1/equipment/cpe/"
    url = f"{service_a_config.base_url}{method_url}{equipment_id}"

    try:
        resp = httpx.post(url, json=set_equipment_request, timeout=180)
    except httpx.TimeoutException:
        if is_retry_task(task):
            raise task.retry() from None
        return {"code": 500, "message": "TimeoutError"}

    if resp.is_server_error and is_retry_task(task):
        raise task.retry()

    result: dict[str, Any] = resp.json()

    return result


def is_retry_task(task: "Task[..., Any]") -> bool:
    if task.max_retries is None:
        return False
    return task.request.retries < task.max_retries
