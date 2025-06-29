import asyncio
from random import random

from equipment_cpe.service_a.exceptions import (
    EquipmentNotFoundError,
    InternalServierError,
)
from equipment_cpe.service_a.models import SetCpeRequest


async def set_equipment_cpe(equipment_id: str, set_cpe_request: SetCpeRequest) -> None:
    error_probability = random()  # noqa: S311 for stab goal
    internal_probability = 0.9
    not_found_probability = 0.9
    if error_probability > internal_probability:
        raise InternalServierError("Internal provisioning exception")

    if error_probability > not_found_probability:
        raise EquipmentNotFoundError("The requested equipment is not found")

    await asyncio.sleep(60)
