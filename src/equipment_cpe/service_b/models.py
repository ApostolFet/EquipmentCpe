from pydantic import BaseModel


class CpeParameter(BaseModel):
    username: str
    password: str
    interfaces: list[int]
    vlan: str | None = None


class SetCpeRequest(BaseModel):
    timeoutInSeconds: int
    parameters: list[CpeParameter]


class TaskStatusResponse(BaseModel):
    code: int
    message: str


class TaskIdResponse(BaseModel):
    code: int
    taskId: str
