from logging import Logger
from flask_mongoengine import Document
from mongoengine.fields import StringField, ReferenceField, DateTimeField


class UserModel(Document):
    user_id = StringField(db_field='userId', unique= True)
    user_pass = StringField(db_field="userPass")

    meta = {'indexes':[('user_id')]}


class AccessModel(Document):
    user = ReferenceField(UserModel, db_field="user")
    token = StringField(db_field="token")
    expiration = DateTimeField(db_field="expiration")
