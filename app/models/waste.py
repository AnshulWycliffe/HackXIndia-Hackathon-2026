from mongoengine import (
    Document, StringField, FloatField, BooleanField,
    DateTimeField, ListField, DictField, ReferenceField
)
from datetime import datetime
from app.config.roles import Roles

from app.config.constants import WASTE_CATEGORIES,WASTE_STATUS
from zoneinfo import ZoneInfo
IST = ZoneInfo("Asia/Kolkata")


class Waste(Document):    
    category = StringField(choices=WASTE_CATEGORIES)
    quantity = FloatField()
    facility_id = ReferenceField("User")
    status = StringField(choices=WASTE_STATUS)
    storage_location = StringField()
    collected_by = ReferenceField("User")
    disposed_by = ReferenceField("User")
    disposal_method = StringField()
    issue_type = StringField()
    remarks = StringField()
    created_at = DateTimeField(default=lambda: datetime.now(IST))
    
   