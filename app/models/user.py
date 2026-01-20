from mongoengine import (
    Document, StringField, EmailField, BooleanField,
    DateTimeField, ListField, DictField, ReferenceField
)
from datetime import datetime
from app.config.roles import Roles
from app.config.constants import ACCOUNT_STATUS
from zoneinfo import ZoneInfo
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

IST = ZoneInfo("Asia/Kolkata")


class User(UserMixin,Document):
    meta = {
        "collection": "users",
        "indexes": ["email", "role", "status"]
    }
    
    # ---- Auth / Core ----
    email = EmailField(required=True, unique=True)
    password_hash = StringField(required=True)
    role = StringField(required=True, choices=Roles.ALL)
    is_active = BooleanField(default=True)
    status = StringField(default=ACCOUNT_STATUS[0], choices=ACCOUNT_STATUS)
    created_at = DateTimeField(default=lambda: datetime.now(IST))
    details = DictField(default=dict)
    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)