from factory import db
from pydantic import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), index=True)

    wishlists = db.relationship("Wishlist", back_populates="user", lazy="dynamic")

    def __repr__(self) -> str:
        return f"<User {self.name}>"
    
    @property
    def password(self) -> str:
        raise AttributeError("Password is a not a readable attribute.")

    @password.setter
    def password(self, password) -> str:
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class CreateUser(BaseModel):
    name: str
    password: str