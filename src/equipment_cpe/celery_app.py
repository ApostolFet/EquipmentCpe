from celery import Celery

from equipment_cpe.config import CeleryConfig


def create_app() -> Celery:
    config = CeleryConfig.load_config()
    return Celery(
        "tasks",
        broker=config.broker_url,
        backend="rpc://",
        include=["equipment_cpe.service_b.tasks"],
    )


celery_app = create_app()
