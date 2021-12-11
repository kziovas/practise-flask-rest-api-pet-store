from flask import Blueprint

home_bp = Blueprint("home_view", __name__)


@home_bp.route("/")
def home():
    return "Welcome to Petstore"
