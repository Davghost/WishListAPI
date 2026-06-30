from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from .wishlist_item import WishlistItemResponse


class ResponseBase(BaseModel):
    def to_response_dict(self):
        return self.model_dump(mode="json")


class OrmBase(ResponseBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class WishlistResponse(OrmBase):
    name: str
    created_at: Optional[str] = None
    wishlist_items: List[WishlistItemResponse] = []


class WishlistCreate(BaseModel):
    name: str


class WishlistUpdate(BaseModel):
    name: str


class WishlistList(ResponseBase):
    wishlists: List[WishlistResponse]


class WishlistMessage(BaseModel):
    id: int
    msg: str
