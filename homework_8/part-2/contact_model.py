from mongoengine import Document, connect
from mongoengine.fields import StringField, BooleanField

connect(host="mongodb://127.0.0.1:27017/my_db")


class Contact(Document):
    fullname = StringField()
    email = StringField()
    phone = StringField()
    sending = BooleanField(default=False)
    email_priority = BooleanField(default=False)
