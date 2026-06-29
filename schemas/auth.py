from pydantic import BaseModel

class LoginResponseMessage(BaseModel):
    access_token: str