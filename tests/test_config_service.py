import os
import pytest
from dotenv import load_dotenv
from core import ConfigService


def test_dev_config_service():
    """This test ensures that the dev config service can read the environment variables
    which define the location of the config.json files"""

    load_dotenv("env/dev.env")
    config_service = ConfigService()
    config_service.load()
    assert config_service.config_folder_path != None
    assert config_service.config_folder_name != None

def test_prod_config_service():
    """This test ensures that the prod config service can read the environment variables
    which define the location of the config.json files"""

    load_dotenv("env/prod.env")
    config_service = ConfigService()
    config_service.load()
    assert config_service.config_folder_path != None
    assert config_service.config_folder_name != None
