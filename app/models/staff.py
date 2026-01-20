from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    DateTimeField
)
from datetime import datetime
from .user import User


class StaffProfile(Document):
    user = ReferenceField(User, required=True)
    department = StringField()
    employee_id = StringField(unique=True)

    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "staff",
        "indexes": ["employee_id"]
    }
