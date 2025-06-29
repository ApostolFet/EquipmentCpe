from pydantic import BaseModel


class CpeParameter(BaseModel):
    username: str
    password: str
    interfaces: list[int]
    vlan: str | None = None


class SetCpeRequest(BaseModel):
    timeoutInSeconds: int
    parameters: list[CpeParameter]


class SetCpeResponse(BaseModel):
    code: int
    message: str
