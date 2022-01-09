import json
from logging import Logger
from flask import Flask
from flask_mongoengine import MongoEngine
from api.authentication_view import AcessController
from core import ConfigService
from injector import singleton, inject
from api import home_bp, PetsController, UserController, AcessController


@singleton
class PetStore:
    @inject
    def __init__(
        self,
        logger: Logger,
        mongo_engine: MongoEngine,
        config_service: ConfigService,
        pets_view_manager: PetsController,
        user_controller: UserController,
        access_controller: AcessController
    ) -> None:
        self.logger = logger
        self.mongo_engine = mongo_engine
        self.config_service = config_service
        self.pets_view_manager = pets_view_manager
        self.user_controller = user_controller
        self.access_controller = access_controller

    def create_app(self, name: str = "PetStore"):
        app = Flask(name)
        try:
            self.config_service.load()
        except Exception as exc:
            self.logger.error(f"Loading configuration file failed due to: {exc}")
            raise exc

        #Load app settings
        with open(self.config_service.flask_settings_filepath) as f:
            settings = json.load(f)

        app.config.update(settings)
        #app.config['MONGODB_SETTINGS'] = {
        #    'host':'mongodb://petstore_mongo/petstore'
        #}

        self.mongo_engine.init_app(app)

        #Initiliaze configuration and URL rules for all views
        self.pets_view_manager.configure()
        self.user_controller.configure()
        self.access_controller.configure()

        #Register blueprints
        app.register_blueprint(home_bp)
        app.register_blueprint(self.pets_view_manager.pets_bp)
        app.register_blueprint(self.user_controller.user_bp)
        app.register_blueprint(self.access_controller.access_bp)

        return app
