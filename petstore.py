from logging import Logger
from flask import Flask
from flask_mongoengine import MongoEngine
from core import ConfigService
from injector import singleton, inject
from home.views import home_app


@singleton
class PetStore:
    @inject
    def __init__(
        self, logger: Logger, mongo_engine: MongoEngine, config_service: ConfigService
    ) -> None:
        self.logger = logger
        self.mongo_engine = mongo_engine
        self.config_service = config_service

    def create_app(self, name: str = "PetStore"):
        app = Flask(name)
        try:
            self.config_service.load()
        except Exception as exc:
            self.logger.error(f"Loading configuration file failed due to: {exc}")

        self.mongo_engine.init_app(app)
        app.register_blueprint(home_app)

        return app
