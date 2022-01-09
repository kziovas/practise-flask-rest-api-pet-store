from functools import wraps
from flask import request, jsonify
from http import HTTPStatus
from datetime import datetime
from shared import USER_ID, USER_TOKEN
from models import UserModel, AccessModel


def authenticator(func):
    @wraps(func)
    def auth_decorated(*args, **kwargs):
        user_id = request.headers.get(USER_ID)
        user_token = request.headers.get(USER_TOKEN)

        if  user_id is None or  user_token is None :
            return jsonify({}), HTTPStatus.FORBIDDEN

        current_user:UserModel = UserModel.objects.filter(user_id=user_id).first()
        if not current_user:
            return jsonify({}), HTTPStatus.FORBIDDEN

        access:AccessModel = AccessModel.objects.filter(user=current_user).first()
        if not access or access.token != user_token:
            return jsonify({}), HTTPStatus.FORBIDDEN
        elif access.expiration < datetime.utcnow():
             return jsonify({'error': "TOKEN has expired"}), HTTPStatus.FORBIDDEN

        print("Access granted")

        return func(*args, **kwargs)
    return  auth_decorated