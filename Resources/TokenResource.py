from flask import request
from flask_restful import Resource
from models.users import User
from flask_jwt_extended import create_access_token
from utils import check_password
from http import HTTPStatus


class TokenResource(Resource):

    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.get_by_email(email=email)

        if not user or not check_password(password, user.password):
            return {'message': 'email or password incorrect'}, HTTPStatus.UNAUTHORIZED

        access_token = create_access_token(identity=user.id)

        return {'access token': access_token}, HTTPStatus.OK


