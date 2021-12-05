from flask import Blueprint
from api import PetsController
from injector import singleton, inject


@singleton
class PetsViewManager:
    @inject
    def __init__(self, pets_controller: PetsController) -> None:
        self.pets_view = None
        self.pets_controller = pets_controller

    def configure(self):
        self.pets_view = Blueprint("pets_view", __name__)
        self.pets_view.add_url_rule("/pets/", view_func=PetsController.as_view("pets"))
