from factory import db, api
from spectree import Response
from flask import Blueprint, request
from sqlalchemy import select
from models.wishlist import Wishlist
from models.wishlist_item import WishlistItem
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas.wishlist import (
    WishlistCreate,
    WishlistList,
    WishlistResponse,
    WishlistUpdate,
    WishlistMessage,
)

wishlists_controller = Blueprint("wishlists_controller", __name__, url_prefix="/api/wishlists")


@wishlists_controller.get("/")
@api.validate(resp=Response(HTTP_200=WishlistList, HTTP_404=WishlistMessage), security=[{"bearerAuth": []}], tags=["wishlists"])
@jwt_required()
def get_wishlists():
    """
    Return all wishlists for current user
    """
    current_user = get_jwt_identity()
    wishlists = db.session.scalars(select(Wishlist).filter_by(user_id=current_user)).all()

    if not wishlists:
        return {"id": None, "msg": "There is no wishlists"}, 404

    response = WishlistList(wishlists=[WishlistResponse.model_validate(w) for w in wishlists]).to_response_dict()
    return response, 200


@wishlists_controller.get("/<int:wishlist_id>")
@api.validate(resp=Response(HTTP_200=WishlistResponse, HTTP_404=WishlistMessage), security=[{"bearerAuth": []}], tags=["wishlists"])
@jwt_required()
def get_wishlist(wishlist_id):
    """
    Get wislist
    """
    current_user = get_jwt_identity()
    wishlist = db.session.get(Wishlist, wishlist_id)

    if not wishlist or wishlist.user_id != current_user:
        return {"id": None, "msg": f"There is no wishlist with id {wishlist_id}"}, 404

    response = WishlistResponse.model_validate(wishlist).to_response_dict()
    return response, 200


@wishlists_controller.post("/")
@api.validate(json=WishlistCreate, resp=Response(HTTP_201=WishlistMessage), security=[{"bearerAuth": []}], tags=["wishlists"])
@jwt_required()
def post_wishlist():
    """
    Create a new wishlist
    """
    current_user = get_jwt_identity()
    data = request.json

    if db.session.scalars(select(Wishlist).filter_by(name=data["name"], user_id=current_user)).first():
        return {"id": None, "msg": "name not available"}, 409

    wishlist = Wishlist(name=data["name"], user_id=current_user)
    db.session.add(wishlist)
    db.session.commit()

    return WishlistMessage(id=wishlist.id, msg="Wishlist created successfully").model_dump(), 201


@wishlists_controller.put("/<int:wishlist_id>")
@api.validate(json=WishlistUpdate, resp=Response(HTTP_200=WishlistResponse, HTTP_404=WishlistMessage), security=[{"bearerAuth": []}], tags=["wishlists"])
@jwt_required()
def put_wishlist(wishlist_id):
    """
    Put wishlist
    """
    current_user = get_jwt_identity()
    wishlist = db.session.get(Wishlist, wishlist_id)

    if not wishlist or wishlist.user_id != current_user:
        return {"id": None, "msg": f"There is no wishlist with id {wishlist_id}"}, 404

    data = request.json
    wishlist.name = data["name"]
    db.session.commit()

    response = WishlistResponse.model_validate(wishlist).to_response_dict()
    return response, 200


@wishlists_controller.delete("/<int:wishlist_id>")
@api.validate(resp=Response(HTTP_200=WishlistMessage, HTTP_404=WishlistMessage), security=[{"bearerAuth": []}], tags=["wishlists"])
@jwt_required()
def delete_wishlist(wishlist_id):
    """
    Delete wishlist and all its items
    """
    current_user = get_jwt_identity()
    wishlist = db.session.get(Wishlist, wishlist_id)

    if not wishlist or wishlist.user_id != current_user:
        return {"id": None, "msg": f"There is no wishlist with id {wishlist_id}"}, 404

    db.session.query(WishlistItem).filter_by(wishlist_id=wishlist.id).delete()
    db.session.delete(wishlist)
    db.session.commit()

    return {"id": wishlist.id, "msg": "Wishlist deleted successfully."}, 200
