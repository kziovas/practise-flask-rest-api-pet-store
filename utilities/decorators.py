from functools import wraps
from flask import request, jsonify
from http import HTTPStatus
from shared import USER_ID, USER_PASSWORD


def authenticator(func):
    @wraps(func)
    def auth_decorated(*args, **kwargs):
        user_id = request.headers.get(USER_ID)
        user_password = request.headers.get(USER_PASSWORD)

        if  user_id is None or  user_password is None or (user_id!="ADMIN" and user_password!="MyPets"):
            return jsonify({}), HTTPStatus.FORBIDDEN

        print("Access granted")

        return func(*args, **kwargs)
    return  auth_decorated