import os
import json
from dotenv import load_dotenv
from injector import singleton, inject


@singleton
class ConfigService:
    def __init__(self) -> None:
        self.config_filepath: str = None
        self.safe_key: str = None
        self.log_level: str = None
        self.mongo_host: str = None
        self.mongo_db: str = None
        self.host: str = None
        self.app_port: int = None

    def load(self):
        load_dotenv()
        self.config_filepath = os.environ["CONFIG_FILE_PATH"]

        with open(self.config_filepath, "r") as config_file:
            config_data = json.load(config_file)

            self.safe_key = config_data["SAFE_PASSWORD"]
            self.log_level = config_data["LOG_LEVEL"]
            self.mongo_host = config_data["MONGODB_HOST"]
            self.mongo_db = config_data["MONGODB_DB"]
            self.host = config_data["HOST"]
            self.app_port = int(config_data["APP_PORT"])
            del config_data
