from factory import db
from datetime import datetime, timezone

class Wishlist(db.Model):
    __tablename__ = "wishlist"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="wishlists")

    wishlist_items = db.relationship("WishlistItem", back_populates="wishlist", lazy="dynamic")

    def __repr__(self) -> str:
        return f"<Wishlist {self.name}>"