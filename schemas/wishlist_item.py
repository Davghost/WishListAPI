from pydantic import BaseModel, ConfigDict
from typing import Optional

class ResponseBase(BaseModel):
    def to_response_dict(self):
        return self.model_dump(mode="json")

class OrmBase(ResponseBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class WishListItemCreate(OrmBase):
    name: str
    description: Optional[str]
    link: Optional[str]
    purchased: bool
    sort_order: int

class WishListItensList(OrmBase):
    itens: list[WishListItemCreate]