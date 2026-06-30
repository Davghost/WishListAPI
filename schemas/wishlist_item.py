from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class ResponseBase(BaseModel):
    def to_response_dict(self):
        return self.model_dump(mode="json")


class OrmBase(ResponseBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class WishlistItemResponse(OrmBase):
    name: str
    description: Optional[str] = None
    link: Optional[str] = None
    wishlist_id: int
    purchased: bool
    sort_order: Optional[int] = None


class WishlistItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    link: Optional[str] = None
    sort_order: Optional[int] = None
    wishlist_id: int


class WishlistItemUpdate(BaseModel):
    name: str
    description: Optional[str] = None
    link: Optional[str] = None
    purchased: bool
    sort_order: Optional[int] = None


class WishlistItemsList(ResponseBase):
    itens: List[WishlistItemResponse]


class WishlistItemMessage(BaseModel):
    id: int
    msg: str
