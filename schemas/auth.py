from pydantic import BaseModel


class CreateUser(BaseModel):
    name: str
    password: str


class LoginRequest(BaseModel):
    name: str
    password: str


class LoginResponseMessage(BaseModel):
    access_token: str


class UserResponse(BaseModel):
    id: int
    name: str


class CreateUserResponse(UserResponse):
    msg: str