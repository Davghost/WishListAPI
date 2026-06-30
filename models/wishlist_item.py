from factory import db
from sqlalchemy import text

class WishlistItem(db.Model):
    __tablename__ = "wishlistitem"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    link = db.Column(db.String(255), nullable=True)
    purchased = db.Column(db.Boolean, server_default=text("false"), nullable=False)
    sort_order = db.Column(db.Integer, nullable=True)

    wishlist_id = db.Column(db.Integer, db.ForeignKey("wishlist.id"), nullable=False)
    wishlist = db.relationship("Wishlist", back_populates="wishlist_items")

    def __repr__(self) -> str:
        return f"<Item {self.name}>"