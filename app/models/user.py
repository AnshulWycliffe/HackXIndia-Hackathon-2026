from mongoengine import Document, StringField, EmailField

class User(Document):
    email = EmailField(required=True)
    password = StringField(required=True)
    role = StringField(required=True)

    def verify_password(password):
        return True