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
    temp_storage = StringField(required=True, choices=Roles.ALL)
    facility_id = ReferenceField()
    status = StringField(choices=WASTE_STATUS)
    collected_by = ReferenceField()
    disposed_by = ReferenceField()
    disposal_method = StringField()
    created_at = DateTimeField(default=lambda: datetime.now(IST))
    
   