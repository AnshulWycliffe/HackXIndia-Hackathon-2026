from mongoengine import Document, StringField, DateTimeField, ReferenceField
from datetime import datetime
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")

class AuditLog(Document):
    action = StringField(required=True)
    actor_role = StringField(required=True)
    actor_id = ReferenceField("User")
    target_type = StringField()   # waste / user
    target_id = StringField()     # id as string
    message = StringField()
    created_at = DateTimeField(default=lambda: datetime.now(IST))
