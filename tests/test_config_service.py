import os
import pytest
from dotenv import load_dotenv
from core import ConfigService


def test_config_service():
    """This test ensures that the config service can read the environment variables
    which define the location of the config.json files"""

    load_dotenv("env/common.env")
    config_service = ConfigService()
    config_service.load()
    config_service.config_folder_path != None
    config_service.config_folder_name != None
