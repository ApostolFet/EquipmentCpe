from logging import getLogger

from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse

from equipment_cpe.service_a.domain import set_equipment_cpe
from equipment_cpe.service_a.models import SetCpeRequest, SetCpeResponse

router = APIRouter(prefix="/equipment")
logger = getLogger(__name__)


@router.post("/cpe/{equipment_id}")
async def set_cpe(equipment_id: str, set_cpe_request: SetCpeRequest) -> SetCpeResponse:
    await set_equipment_cpe(equipment_id, set_cpe_request)
    return SetCpeResponse(code=200, message="success")


def equipment_not_found_hander(request: Request, exc: Exception) -> Response:
    equipment_id = request.path_params.get("id")
    logger.info("Client Error: %s with %s", exc, equipment_id)
    return JSONResponse(
        status_code=404,
        content={
            "code": 404,
            "message": str(exc),
        },
    )


def internal_error_hander(request: Request, exc: Exception) -> Response:
    equipment_id = request.path_params.get("id")
    logger.error("Server Error: %s with %s", exc, equipment_id)
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": "Internal provisioning exception",
        },
    )
