import os
from dataclasses import dataclass
from typing import Self


class LoadConfigError(Exception): ...


@dataclass
class CeleryConfig:
    broker_url: str

    @classmethod
    def load_config(cls) -> Self:
        broker_url = os.getenv("BROKER_URL")
        if broker_url is None:
            raise LoadConfigError("BROKER_URL is not setup")
        return cls(broker_url=broker_url)


@dataclass
class SeriveceAConfig:
    base_url: str

    @classmethod
    def load_config(cls) -> Self:
        base_url = os.getenv("SERVICE_A_BASE_URL")
        if base_url is None:
            raise LoadConfigError("SERVICE_A_BASE_URL is not setup")
        return cls(base_url=base_url)
