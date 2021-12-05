from http import HTTPStatus
from flask.views import MethodView
from flask import Blueprint
from injector import singleton, inject
from flask import jsonify, abort, request


@singleton
class PetsController(MethodView):
    pets = [
        {"id": 1, "name": "Banu"},
        {"id": 2, "name": "Orfeas"},
        {"id": 3, "name": "Shiba"},
    ]

    @inject
    def __init__(self) -> None:
        super().__init__()

    def configure(self):
        self.pets_view = Blueprint("pets_view", __name__)
        self.pets_view.add_url_rule("/pets/", view_func=PetsController.as_view("pets"))

    def get(self):
        return jsonify({"pets": self.pets})

    def post(self):
        if not request.json or not "name" in request.json:
            return (
                f"Data missing from POST request {request.json}",
                HTTPStatus.BAD_REQUEST,
            )

        new_pet = {"id": len(self.pets) + 1, "name": request.json["name"]}
        self.pets.append(new_pet)
        return jsonify(message=f"new pet added: {self.pets}"), HTTPStatus.CREATED
