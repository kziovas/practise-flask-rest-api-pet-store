import os
import json
from pathlib import Path
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
        self.config_folder_path: str = None
        self.config_folder_name: str = None

    def load(self):
        self.config_folder_name = os.environ["CONFIG_FOLDER_NAME"]
        self.config_folder_path = (
            Path(__file__).parents[1].absolute().joinpath(self.config_folder_name)
        )
        self.config_filepath = self.config_folder_path.joinpath(
            os.environ["CONFIG_FILE_NAME"]
        )

        with open(self.config_filepath, "r") as config_file:
            config_data = json.load(config_file)

            self.safe_key = config_data["SAFE_PASSWORD"]
            self.log_level = config_data["LOG_LEVEL"]
            self.mongo_host = config_data["MONGODB_HOST"]
            self.mongo_db = config_data["MONGODB_DB"]
            self.host = config_data["HOST"]
            self.app_port = int(config_data["APP_PORT"])
            del config_data


if __name__ == "__main__":
    config_service = ConfigService()
    config_service.load()
    print(config_service.safe_key)
