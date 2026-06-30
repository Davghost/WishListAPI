from flask import Blueprint, request
from factory import db, api
from spectree import Response
from sqlalchemy import select
from models.user import User, CreateUser
from flask_jwt_extended import create_access_token
from schemas.utils_response import DefaultRespose
from schemas.auth import LoginResponseMessage

user_controller = Blueprint("user_controller", __name__, url_prefix="/users")



@user_controller.post("/")
@api.validate(json=CreateUser, resp=Response(HTTP_201=DefaultRespose), security={}, tags=["users"])
def create_user():
    """
    Create user
    """
    data = request.json

    if db.session.scalars(
        select(User).filter_by(name=data["name"])
    ).first():
        return {"id": None, "msg": "Name not available"}, 409
    
    #user = db.session.scalars(select(User).filter_by(name=data["name"])).first()
    
    user = User(name=data["name"])
    user.password = data["password"]

    db.session.add(user)
    db.session.commit()

    return {"id": user.id, "msg": "User created successfully."}, 201

@user_controller.post("/login")
@api.validate(json=CreateUser, resp=Response(HTTP_200=LoginResponseMessage, HTTP_401=DefaultRespose),security={}, tags=["users"])
def login():
    """
    Login
    """
    data = request.json

    user = db.session.scalars(select(User).filter_by(name=data["name"])).first()

    if user and user.verify_password(data["password"]):
        return {
            "access_token": create_access_token(
                identity=user.id, expires_delta=None
            )
        }, 200
    
    return {"id": None, "msg": "Name and password do not match."}, 401