from fastapi import FastAPI

from equipment_cpe.service_a.exceptions import EquipmentNotFoundError
from equipment_cpe.service_a.routes import (
    equipment_not_found_hander,
    internal_error_hander,
    router,
)
from equipment_cpe.service_b.routes import router as b_router


def create_app() -> FastAPI:
    app = FastAPI(title="Serivice A", root_path="/api/v1")
    app.include_router(router)
    app.include_router(b_router)
    app.exception_handler(Exception)(internal_error_hander)
    app.exception_handler(EquipmentNotFoundError)(equipment_not_found_hander)
    return app
