import bcrypt
import uuid
from datetime import datetime, timedelta
from flask.views import MethodView
from http import HTTPStatus
from flask import request, abort, jsonify
from models import UserModel, AccessModel
from shared import USER_ID, USER_PASSWORD, TOKEN


class UserController(MethodView):
    def __init__(self) -> None:
        super().__init__()
        if not request.json:
            abort(HTTPStatus.BAD_REQUEST.value)

    def post(self):
        if  not USER_ID is request.json or  not USER_PASSWORD is request.json:
            return jsonify({"message":"Missing user_id or password"}), HTTPStatus.BAD_REQUEST
        existing_user = UserModel.__objects.filter(user_id=request.json.get(USER_ID)).first()

        if existing_user:
            return jsonify({"message":"User id already exists"}), HTTPStatus.BAD_REQUEST
        else:
            # create encrypted credentials
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(request.json.get(USER_PASSWORD), salt)
            user = UserModel(
                user_id=request.json.get(USER_ID),
                user_passwordl=hashed_password
            ).save()
            return jsonify({'result': 'User has been registered'}), HTTPStatus.OK

class AcessController(MethodView):
    def __init__(self) -> None:
        super().__init__()
        if not request.json:
            abort(HTTPStatus.BAD_REQUEST.value)

    def post(self):
        if  not USER_ID is request.json or not USER_PASSWORD is request.json:
            return jsonify({"message":"Missing user id or password"}), HTTPStatus.BAD_REQUEST
        user = UserModel.__objects.filter(user_id=request.json.get(USER_ID)).first()

        if not user:
            return jsonify({"message":"Wrong credentials"}), HTTPStatus.FORBIDDEN
        else:
            # generate a token
            if bcrypt.hashpw(request.json.get(USER_PASSWORD)) == user.user_password:
                # delete existing tokens
                existing_tokens = AccessModel.__objects.filter(user=user).delete()
                token = str(uuid.uuid4())
                now = datetime.utcnow().replace(second=0, microsecond=0)
                expires = now + timedelta(days=30)
                access = AccessModel(
                    user=user,
                    token=token,
                    expires=expires
                ).save()
                expires_formated = expires.isoformat("T") + "Z"
                return jsonify({'New token created ': token, 'Token expires': expires_formated}), HTTPStatus.OK
            else:
     
                return jsonify({'message': "Wrong creadentials provided!"}), HTTPStatus.FORBIDDEN