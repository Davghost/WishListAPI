from pydantic import BaseModel
from typing import Optional


class DefaultRespose(BaseModel):
    id: Optional[int] = None
    msg: str