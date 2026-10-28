"""
Account Model
"""
from datetime import date
from service import db


class Account(db.Model):
    """Model for a Customer Account"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(256))
    phone_number = db.Column(db.String(32))
    date_joined = db.Column(db.Date())

    def serialize(self):
        """Serialize an Account into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "phone_number": self.phone_number,
            "date_joined": str(self.date_joined) if self.date_joined else None,
        }

    def deserialize(self, data):
        """Deserialize an Account from a dictionary"""
        self.name = data["name"]
        self.email = data["email"]
        self.address = data.get("address")
        self.phone_number = data.get("phone_number")
        raw = data.get("date_joined")
        self.date_joined = date.fromisoformat(raw) if isinstance(raw, str) else raw
        return self
