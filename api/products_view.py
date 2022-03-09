import uuid
import json
from jsonschema import validate
from jsonschema import exceptions as schema_exceptions
from datetime import datetime, timedelta
from utilities import authenticator
from flask.views import MethodView
from http import HTTPStatus
from flask import request, Blueprint, abort, jsonify
from injector import singleton, inject
from models import ProductModel
from shared import PAGE_OBJECT_LIMIT, PAGE_LIMIT, PRODUCT_ID
from schemas import product_schema


@singleton
class ProductController(MethodView):
    decorators = [authenticator]

    @inject
    def __init__(self) -> None:
        super().__init__()

    def configure(self):
        self.product_bp = Blueprint("products_view", __name__)
        self.products_view = ProductController.as_view("products")
        self.product_bp.add_url_rule(
            "/products/",
            defaults={"product_name": None},
            view_func=self.products_view,
            methods=[
                "GET",
            ],
        )
        self.product_bp.add_url_rule(
            "/products/",
            view_func=self.products_view,
            methods=[
                "POST",
            ],
        )
        self.product_bp.add_url_rule(
            "/products/<product_name>",
            view_func=self.products_view,
            methods=["GET", "PUT", "DELETE"],
        )

    def post(self):
        if not request.json:
            abort(HTTPStatus.BAD_REQUEST.value)

        try:
            validate(request.json, product_schema)
            existing_product = ProductModel.objects.filter(
                product_name=request.json.get("product_name")
            ).first()

            if existing_product:
                return (
                    jsonify({"message": "Product name already exists"}),
                    HTTPStatus.BAD_REQUEST,
                )
            else:
                # add product to database
                product = ProductModel(
                    product_id=str(uuid.uuid4()),
                    product_name=request.json.get("product_name"),
                    price=request.json.get("price"),
                    stock=request.json.get("stock"),
                ).save()
                return jsonify({"result": "Product has been registered"}), HTTPStatus.OK
        except schema_exceptions.ValidationError as ex:
            return (
                jsonify({"message": "Missing product_name, price or stock"}),
                HTTPStatus.BAD_REQUEST,
            )

    def put(self, product_name):
        if product_name:
            product: ProductModel = None
            try:
                product = ProductModel.objects.filter(product_name=product_name).first()
                body = request.get_json()
                product.update(**body)
                product = ProductModel.objects.filter(product_name=product_name).first()
                return jsonify({"product": product}), HTTPStatus.OK
            except Exception as exc:
                return (
                    f"The product name provided: {product_name}, does not exist",
                    HTTPStatus.BAD_REQUEST,
                )
        else:

            return jsonify({"product": {}}), HTTPStatus.OK

    def get(self, product_name):
        if product_name:
            product: ProductModel = None
            try:
                product = ProductModel.objects.filter(product_name=product_name).first()
                return jsonify({"product": product}), HTTPStatus.OK
            except Exception as exc:
                return (
                    f"The product name provided: {product_name}, does not exist",
                    HTTPStatus.BAD_REQUEST,
                )

        else:
            products = ProductModel.objects()
            products_dict = {}
            try:
                for index, product in enumerate(products):
                    response_product = product.to_json()
                    # response_product.pop("_id")
                    # response_product.pop(PRODUCT_ID)
                    products_dict[f"product_{index}"] = response_product
            except StopIteration:
                pass
            finally:
                return jsonify(products_dict), HTTPStatus.OK

    def delete(self, product_name):
        if product_name:
            product: ProductModel = None
            try:
                product = ProductModel.objects.filter(product_name=product_name).first()
                return jsonify({"product": product}), HTTPStatus.OK
            except Exception as exc:
                return (
                    f"The product name provided: {product_name}, does not exist",
                    HTTPStatus.BAD_REQUEST,
                )
            finally:
                if product:
                    product.delete()
