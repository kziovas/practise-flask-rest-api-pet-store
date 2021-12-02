from flask import Flask
from flask_mongoengine import MongoEngine
from core import ConfigService
from injector import singleton, inject
from home.views import home_app


@singleton
class PetStore:
    def __init__(
        self, mongo_engine: MongoEngine, config_service: ConfigService
    ) -> None:
        self.mongo_engine = mongo_engine
        self.config_service = config_service

    def create_app(self, name: str = "PetStore"):
        app = Flask(name)
        self.config_service.load()
        self.mongo_engine.init_app(app)
        app.register_blueprint(home_app)
