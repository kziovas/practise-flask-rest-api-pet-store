import logging
import os
from flask_mongoengine import MongoEngine
from logging import Logger
from injector import Module, inject, singleton, provider


class CoreModule(Module):
    @singleton
    @provider
    def provide_mongo_engine(self) -> MongoEngine:
        mongo_engine = MongoEngine()

        return mongo_engine

    @singleton
    @provider
    def provide_logger(self) -> Logger:
        log_level = logging.INFO
        if os.getenv("LOG_LEVEL") == "DEBUG":
            log_level = logging.DEBUG

        logger = logging.getLogger(name="petstore")
        logger.setLevel(log_level)

        # Create handlers
        stream_handler = logging.StreamHandler()
        file_handler = logging.FileHandler("petstore.log")
        stream_handler.setLevel(log_level)
        file_handler.setLevel(log_level)

        # Create formatters and add it to handlers
        stream_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        file_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        stream_handler.setFormatter(stream_format)
        file_handler.setFormatter(file_format)

        # Add handlers to the logger
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

        return logger
