# models.py:
from mongoengine import Document, \
    StringField, \
    BooleanField


class Contact(Document):
    fullname = StringField()
    email = StringField()
    message_sent_status = BooleanField(default=False)


if __name__ == "__main__":
    pass
