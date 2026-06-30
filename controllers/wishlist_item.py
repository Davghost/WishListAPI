from factory import db, api
from spectree import Response
from flask import Blueprint, jsonify
from sqlalchemy import select
from models.wishlist_item import WishlistItem
from models.wishlist import Wishlist
from flask.globals import request
from schemas.wishlist_item import (
    WishlistItemCreate,
    WishlistItemsList,
    WishlistItemUpdate,
    WishlistItemResponse,
    WishlistItemMessage,
)
from flask_jwt_extended import jwt_required, get_jwt_identity

wishlist_controller = Blueprint("wishlist_controller", __name__, url_prefix="/api/wishlist")

@wishlist_controller.get("/")
@api.validate(resp=Response(HTTP_200=WishlistItemsList, HTTP_404=WishlistItemMessage), tags=["wishlist"])
@jwt_required()
def getall_itens():
    """
    Return all itens
    """
    current_user = get_jwt_identity()
    itens = db.session.scalars(
        select(WishlistItem).join(Wishlist).filter(Wishlist.user_id == current_user)
    ).all()

    if not itens:
        return {"id": None, "msg": "There is no itens"}, 404
    
    #return jsonify(
    #    [
    #        {
    #            "id": item.id,
    #            "name": item.name,
    #            "description": item.description if item.description else None,
    #            "link": item.link if item.link else None,
    #            "purchased": item.purchased,
    #            "sort_order": item.sort_order if item.sort_order else None,
    #        }
    #        for item in itens
    #    ] 
    #), 200

    response = WishlistItemsList(
        itens=[WishlistItemResponse.model_validate(item) for item in itens]
    ).to_response_dict()
    return response, 200

@wishlist_controller.get("/<int:item_id>")
@api.validate(resp=Response(HTTP_200=WishlistItemResponse, HTTP_404=WishlistItemMessage), tags=["wishlist"])
@jwt_required()
def get_item(item_id):
    """
    Return an item
    """
    current_user = get_jwt_identity()
    item = db.session.get(WishlistItem, item_id)

    if item is None or item.wishlist is None or item.wishlist.user_id != current_user:
        return {"id": None, "msg": f"There is no item with id {item_id}"}, 404

    if item is None:
        return {"id": None, "msg": f"There is no item with id {item_id}"}, 404
    
    #return {
    #    "id": item.id,
    #    "name": item.name,
    #    "description": item.description if item.description else None,
    #    "link": item.link if item.link else None,
    #    "purchased": item.purchased,
    #    "sort_order": item.sort_order if item.sort_order else None,
    #}, 200

    response = WishlistItemResponse.model_validate(item).to_response_dict()
    return response, 200

@wishlist_controller.post("/")
@api.validate(json=WishlistItemCreate, resp=Response(HTTP_201=WishlistItemMessage), tags=["wishlist"])
@jwt_required()
def post_item():
    """
    Create an item
    """
    data = request.json

    current_user = get_jwt_identity()

    if db.session.scalars(
        select(WishlistItem).filter_by(name=data["name"])  
    ).first():
        return {"id": None, "msg": "name not available"}, 409

    # wishlist ownership check
    wishlist = db.session.get(Wishlist, data.get("wishlist_id"))
    if not wishlist or wishlist.user_id != current_user:
        return {"id": None, "msg": "Invalid wishlist or access denied."}, 404

    item = WishlistItem(
        name=data["name"],
        description=data["description"] if "description" in data else None,
        link=data["link"] if "link" in data else None,
        purchased=data.get("purchased", False),
        sort_order=data["sort_order"] if "sort_order" in data else None,
        wishlist_id=wishlist.id,
    )

    db.session.add(item)
    db.session.commit()

    response = WishlistItemMessage(id=item.id, msg="Item added in wishlist successfully").model_dump()
    return response, 201

@wishlist_controller.put("/<int:item_id>")
@api.validate(json=WishlistItemUpdate, resp=Response(HTTP_200=WishlistItemResponse, HTTP_404=WishlistItemMessage), tags=["wishlist"])
@jwt_required()
def put_item(item_id):
    """
    Update an item
    """
    current_user = get_jwt_identity()
    item = db.session.get(WishlistItem, item_id)

    if not item or item.wishlist is None or item.wishlist.user_id != current_user:
        return {"id": None, "msg": f"There is no item with id {item_id}"}, 404

    data = request.json

    item.name = data["name"]
    item.description = data["description"] if "description" in data else None
    item.link = data["link"] if "link" in data else None
    item.purchased = data["purchased"]
    item.sort_order = data["sort_order"] if "sort_order" in data else None

    db.session.commit()
    response = WishlistItemResponse.model_validate(item).to_response_dict()
    return response, 200

@wishlist_controller.delete("/<int:item_id>")
@api.validate(resp=Response(HTTP_200=WishlistItemMessage, HTTP_404=WishlistItemMessage), tags=["wishlist"])
@jwt_required()
def delete_item(item_id):
    """
    Delete an item
    """
    current_user = get_jwt_identity()
    item = db.session.get(WishlistItem, item_id)

    if not item or item.wishlist is None or item.wishlist.user_id != current_user:
        return {"id": None, "msg": f"There is no item with id {item_id}"}, 404

    db.session.delete(item)
    db.session.commit()

    return {"id": item.id, "msg": "Item deletado com sucesso."}, 200