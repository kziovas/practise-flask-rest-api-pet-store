from flask_mongoengine import Document
from mongoengine.fields import (
    StringField,
    DateTimeField,
    FloatField,
    IntField,
)
from shared import PRODUCT_ID


class ProductModel(Document):
    product_id = StringField(db_field=PRODUCT_ID, unique=True)
    product_name = StringField(db_field="productName")
    price = FloatField(db_field="price")
    stock = IntField(db_field="stock")
    description = StringField(db_field="description", required=False)
    animal_type = StringField(db_field="animalType", required=False)
    expiration_date = DateTimeField(db_field="epirationDate", required=False)

    meta = {"indexes": [("product_id"), ("product_name")]}
