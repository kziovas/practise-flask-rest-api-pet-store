import os
from petstore import PetStore
from injector import Injector
from core import CoreModule


def main():
    injector = Injector(modules=[CoreModule])
    petstore = injector.get(PetStore)
    app = petstore.create_app()
    app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False
 
    app.run(host=os.getenv("HOST", "0.0.0.0"),port=int(os.getenv("APP_PORT", 8000)))


if __name__ == "__main__":
    main()
