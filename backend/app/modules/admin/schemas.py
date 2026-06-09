from pydantic import BaseModel


class AdminLoginRequest(BaseModel):
    password: str


class AdminTokenSchema(BaseModel):
    token: str
