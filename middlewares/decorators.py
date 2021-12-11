from functools import wraps
from flask import request, jsonify
from http import HTTPStatus


def authenticator(func):
    @wraps(func)
    def auth_decorated(*args, **kwargs):
        user_id = request.headers.get('USER-ID')
        user_token = request.headers.get('USER-TOKEN')

        if  user_id is None or  user_token is None or user_id!="ADMIN" or user_token!="MyPets":
            return jsonify({}), HTTPStatus.FORBIDDEN

        print("Access granted")

        return func(*args, **kwargs)
    return  auth_decorated