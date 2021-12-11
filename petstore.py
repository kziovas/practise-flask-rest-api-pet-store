from logging import Logger
from flask import Flask
from flask_mongoengine import MongoEngine
from core import ConfigService
from injector import singleton, inject
from api import home_bp, PetsController


@singleton
class PetStore:
    @inject
    def __init__(
        self,
        logger: Logger,
        mongo_engine: MongoEngine,
        config_service: ConfigService,
        pets_view_manager: PetsController,
    ) -> None:
        self.logger = logger
        self.mongo_engine = mongo_engine
        self.config_service = config_service
        self.pets_view_manager = pets_view_manager

    def create_app(self, name: str = "PetStore"):
        app = Flask(name)
        try:
            self.config_service.load()
        except Exception as exc:
            self.logger.error(f"Loading configuration file failed due to: {exc}")
            raise exc

        self.mongo_engine.init_app(app)
        self.pets_view_manager.configure()
        app.register_blueprint(home_bp)
        app.register_blueprint(self.pets_view_manager.pets_bp)

        return app
