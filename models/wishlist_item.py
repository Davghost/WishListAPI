from factory import db

class WishListItem(db.Model):
    __tablename__ = "wishlistitem"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    link = db.Column(db.String(255), nullable=True)
    purchased = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, nullable=True)

    def __repr__(self) -> str:
        return f"<Item {self.name}>"