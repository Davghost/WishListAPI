from factory import db, api
from spectree import Response
from flask import Blueprint, jsonify
from sqlalchemy import select
from models.wishlist_item import WishlistItem
from flask.globals import request
from schemas.utils_response import DefaultRespose
from schemas.wishlist_item import WishListItemCreate, WishListItensList, WishListItemUpdated, WishListItemResponse

wishlist_controller = Blueprint("wishlist_controller", __name__, url_prefix="/api/wishlist")

@wishlist_controller.get("/")
@api.validate(resp=Response(HTTP_200=WishListItensList, HTTP_404=DefaultRespose), tags=["wishlist"])
def getall_itens():
    """
    Return all itens
    """
    itens = db.session.scalars(select(WishlistItem)).all()

    if not itens:
        return {"msg": "There is no itens"}, 404
    
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

    response = WishListItensList(
        itens=[WishListItemResponse.model_validate(item) for item in itens]
    ).to_response_dict()
    return response, 200

@wishlist_controller.get("/<int:item_id>")
@api.validate(resp=Response(HTTP_200=WishListItemResponse, HTTP_404=DefaultRespose), tags=["wishlist"])
def get_item(item_id):
    """
    Return an item
    """
    item = db.session.get(WishlistItem, item_id)

    if item is None:
        return {"msg": f"There is no item with id {item_id}"}, 404
    
    #return {
    #    "id": item.id,
    #    "name": item.name,
    #    "description": item.description if item.description else None,
    #    "link": item.link if item.link else None,
    #    "purchased": item.purchased,
    #    "sort_order": item.sort_order if item.sort_order else None,
    #}, 200

    response = WishListItemCreate.model_validate(item).to_response_dict()
    return response, 200

@wishlist_controller.post("/")
@api.validate(json=WishListItemCreate, resp=Response(HTTP_200=WishListItemResponse), tags=["wishlist"])
def post_item():
    """
    Create an item
    """
    data = request.json

    if db.session.scalars(
        select(WishlistItem).filter_by(name=data["name"])
    ).first():
        return {"msg": "name not available"}, 409
    
    item = WishlistItem(
        name = data["name"],
        description = data["description"] if "description" in data else None,
        link = data["link"] if "link" in data else None,
        purchased = data["purchased"],
        sort_order = data["sort_order"] if "sort_order" in data else None
    )

    db.session.add(item)
    db.session.commit()

    return {"msg": "Item added in wishlist wish success"}, 201

@wishlist_controller.put("/<int:item_id>")
@api.validate(json=WishListItemUpdated, resp=Response(HTTP_200=WishListItemResponse, HTTP_404=DefaultRespose), tags=["wishlist"])
def put_item(item_id):
    """
    Update an item
    """
    item = db.session.get(WishlistItem, item_id)

    if not item:
        return {"msg": f"There is no item with id {item_id}"}, 404

    data = request.json
    
    item.name = data["name"]
    item.description = data["description"] if "description" in data else None
    item.link = data["link"] if "link" in data else None
    item.purchased = data["purchased"]
    item.sort_order = data["sort_order"] if "sort_order" in data else None

    db.session.commit()
    return {
        "id": item.id,
        "msg": "Item atualizado com sucesso."
    }, 200

@wishlist_controller.delete("/<int:item_id>")
@api.validate(resp=Response(HTTP_200=DefaultRespose, HTTP_404=DefaultRespose), tags=["wishlist"])
def delete_item(item_id):
    """
    Delete an item
    """
    item = db.session.get(WishlistItem, item_id)

    if not item:
        return {
            "id": item.id,
            "msg": f"There is no item with id {item_id}"
        }, 404
    
    db.session.delete(item)
    db.session.commit()

    return {
        "id": item.id,
        "msg": "Item deletado com sucesso."
    }, 200