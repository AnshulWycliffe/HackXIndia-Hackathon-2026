from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    DateTimeField
)
from datetime import datetime
from .user import User


class FacilityProfile(Document):
    name = StringField(required=True)
    facility_type = StringField(
        choices=["HOSPITAL", "LAB", "CLINIC"],
        required=True
    )

    registration_id = StringField(required=True, unique=True)
    address = StringField(required=True)
    city = StringField(required=True)

    admin_user = ReferenceField(User, required=True)

    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "facilities",
        "indexes": ["registration_id", "city"]
    }
