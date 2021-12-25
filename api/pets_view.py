from http import HTTPStatus
import jmespath
from flask.views import MethodView
from flask import Blueprint
from utilities import authenticator
from injector import singleton, inject
from flask import jsonify, abort, request


@singleton
class PetsController(MethodView):
    decorators = [authenticator]

    pets = [
        {"id": 1, "name": "Banu", "links":[{"rel":"self","href":"/pets/1"}]},
        {"id": 2, "name": "Orfeas", "links":[{"rel":"self","href":"/pets/2"}]},
        {"id": 3, "name": "Shiba", "links":[{"rel":"self","href":"/pets/3"}]},
    ]

    @inject
    def __init__(self) -> None:
        super().__init__()

    def configure(self):
        self.pets_bp = Blueprint("pets_view", __name__)
        self.pets_view = PetsController.as_view("pets")
        self.pets_bp.add_url_rule('/pets/',defaults={'pet_id':None}, view_func=self.pets_view, methods=['GET',])
        self.pets_bp.add_url_rule('/pets/', view_func=self.pets_view, methods=['POST',])
        self.pets_bp.add_url_rule('/pets/<int:pet_id>', view_func=self.pets_view, methods=['GET','PUT','DELETE'])

    def get(self, pet_id):
        if pet_id:
            try:
                pet = [pet for pet in self.pets if pet.get("id")==pet_id][0]
                return jsonify({"pet": pet})
            except Exception as exc:
                return (
                f"The pet id provided: {pet_id}, does not exist",
                HTTPStatus.BAD_REQUEST,
            )
       
        return jsonify({"pets": self.pets})

    def post(self):
        if not request.json or not "name" in request.json:
            return (
                f"Data missing from POST request {request.json}",
                HTTPStatus.BAD_REQUEST,
            )
        new_id=len(self.pets) + 1
        new_pet = {"id": new_id, "name": request.json["name"],"links":[{"rel":"self","href":f"/pets/{new_id}"}] }
        self.pets.append(new_pet)
        return jsonify(message=f"new pet added: {new_pet}"), HTTPStatus.CREATED

    def put(self, pet_id):
        if not request.json or not "name" in request.json:
            return (
                f"Data missing from PUT request {request.json}",
                HTTPStatus.BAD_REQUEST,
            )
        try:
            pet = [pet for pet in self.pets if pet.get("id")==pet_id][0]
            pet["name"] = request.json["name"]

        except Exception as exc:
            return (
            f"The pet id provided: {pet_id}, does not exist",
            HTTPStatus.BAD_REQUEST,
        )

        return jsonify({}), HTTPStatus.NO_CONTENT

    def delete(self,pet_id):
        if pet_id:
            pet = None
            try:
                pet = [pet for pet in self.pets if pet.get("id")==pet_id][0]
                return jsonify({"pet": pet}), HTTPStatus.OK
            except Exception as exc:
                return (
                f"The pet id provided: {pet_id}, does not exist",
                HTTPStatus.BAD_REQUEST,
            )
            finally:
                if pet:
                    self.pets.remove(pet)
             


