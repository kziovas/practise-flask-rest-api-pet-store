from flask.views import MethodView
from flask import jsonify, abort, request
from injector import inject, singleton


@singleton
class PetsController(MethodView):
    @inject
    def __init__(self) -> None:
        super().__init__()
        self.pets = [
            {"id": 1, "name": "Banu"},
            {"id": 2, "name": "Orfeas"},
            {"id": 3, "name": "Shiba"},
        ]

    def get(self):
        return jsonify({"pets": self.pets})
