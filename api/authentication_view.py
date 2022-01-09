import bcrypt
import uuid
from datetime import datetime, timedelta
from flask.views import MethodView
from http import HTTPStatus
from flask import request, Blueprint , abort, jsonify
from models import UserModel, AccessModel
from shared import USER_ID, USER_PASSWORD, USER_TOKEN


class UserController(MethodView):
    def __init__(self) -> None:
        super().__init__()

    def configure(self):
        self.user_bp = Blueprint("users_view", __name__)
        self.users_view = UserController.as_view("users")
        self.user_bp.add_url_rule('/users/', view_func=self.users_view, methods = ['POST',])

    def post(self):
        if not request.json:
            abort(HTTPStatus.BAD_REQUEST.value)
        elif  not USER_ID in request.json or not USER_PASSWORD in request.json:
            return jsonify({"message":"Missing user_id or password"}), HTTPStatus.BAD_REQUEST
        existing_user = UserModel.objects.filter(user_id=request.json.get(USER_ID)).first()

        if existing_user:
            return jsonify({"message":"User id already exists"}), HTTPStatus.BAD_REQUEST
        else:
            # create encrypted credentials
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(request.json.get(USER_PASSWORD).encode('utf-8'), salt)
            user = UserModel(
                user_id=request.json.get(USER_ID),
                user_pass=hashed_password
            ).save()
            return jsonify({'result': 'User has been registered'}), HTTPStatus.OK

class AcessController(MethodView):
    def __init__(self) -> None:
        super().__init__()

    def configure(self):
        self.access_bp = Blueprint("access_view", __name__)
        self.access_view = AcessController.as_view("access")
        self.access_bp.add_url_rule('/users/access/', view_func=self.access_view, methods = ['POST',])

    def post(self):
        if not request.json:
            abort(HTTPStatus.BAD_REQUEST.value)
        elif  not USER_ID in request.json or not USER_PASSWORD in request.json:
            return jsonify({"message":"Missing user id or password"}), HTTPStatus.BAD_REQUEST
        user = UserModel.objects.filter(user_id=request.json.get(USER_ID)).first()

        if not user:
            return jsonify({"message":"Wrong credentials"}), HTTPStatus.FORBIDDEN
        else:
            # generate a token
            user_pass_encoded = user.user_pass.encode('utf-8')
            if bcrypt.hashpw(request.json.get(USER_PASSWORD).encode('utf-8'), user_pass_encoded) == user.user_pass.encode('utf-8'):
                # delete existing tokens
                existing_tokens = AccessModel.objects.filter(user=user).delete()
                token = str(uuid.uuid4())
                now = datetime.utcnow().replace(second=0, microsecond=0)
                expiration = now + timedelta(days=30)
                access = AccessModel(
                    user=user,
                    token=token,
                    expiration=expiration
                ).save()
                expiration_formated = expiration.isoformat("T") + "Z"
                return jsonify({'New token created ': token, 'Token expiration': expiration_formated}), HTTPStatus.OK
            else:
     
                return jsonify({'message': "Wrong creadentials provided!"}), HTTPStatus.FORBIDDEN