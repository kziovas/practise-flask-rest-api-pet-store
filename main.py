import os
from flask_script import Manager, Server
from petstore import PetStore
from injector import Injector
from core import CoreModule


def main():
    injector = Injector(modules=[CoreModule])
    petstore = injector.get(PetStore)
    app = petstore.create_app()
    app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False
    manager = Manager(app)

    manager.add_command(
        "runserver",
        Server(
            use_debugger=True,
            use_reloader=True,
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("APP_PORT", 8000)),
        ),
    )

    manager.run()


if __name__ == "__main__":
    main()
