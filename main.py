import os
from flask_script import Manager, Server
from petstore import create_app


def main():
    app = create_app()
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
