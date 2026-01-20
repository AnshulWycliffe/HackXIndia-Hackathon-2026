from mongoengine import (
    Document, StringField, EmailField, BooleanField,
    DateTimeField, ListField, DictField, ReferenceField
)
from datetime import datetime
from app.config.roles import Roles
from app.config.constants import FACILITY_TYPES
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")


class User(Document):
    meta = {
        "collection": "users",
        "indexes": ["email", "role", "status"]
    }

    # ---- Auth / Core ----
    email = EmailField(required=True, unique=True)
    password_hash = StringField(required=True)
    role = StringField(required=True, choices=Roles.ALL)
    is_active = BooleanField(default=True)
    status = StringField(default="PENDING", choices=("PENDING", "ACTIVE", "SUSPENDED", "REVOKED"))
    created_at = DateTimeField(default=lambda: datetime.now(IST))
    approved_by = ReferenceField("self", null=True)
    approved_at = DateTimeField()

    # ---- FACILITY / Generator ----
    organization_name = StringField()
    organization_type = StringField(choices=FACILITY_TYPES)  # HOSPITAL / LAB / CLINIC
    license_number = StringField()
    license_document = StringField()  # Supabase path
    address = StringField()
    geo_location = DictField()  # { lat, lng }
    waste_categories = ListField(StringField())
    max_capacity_per_day = StringField()
    assigned_zone = StringField()

    # ---- COLLECTOR ----
    vehicle_id = StringField()
    contact_number = StringField()
    assigned_zone_collector = StringField()

    # ---- DISPOSAL ----
    facility_name = StringField()
    treatment_types = ListField(StringField())
    capacity_per_day = StringField()
    geo_location_disposal = DictField()  # For routing

    # ---- Utility Methods ----
    def is_approved(self):
        return self.status == "ACTIVE"
