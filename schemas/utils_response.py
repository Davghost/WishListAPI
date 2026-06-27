from pydantic import BaseModel

class DefaultRespose(BaseModel):
    id: int
    msg: str