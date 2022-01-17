from http import HTTPStatus

from flask import jsonify, make_response
from flask_restful import Resource, reqparse

from app import models

sign_up_parser = reqparse.RequestParser()
sign_up_parser.add_argument("login", dest="login", location="json", required=True, type=str, help="The user's login")
sign_up_parser.add_argument(
    "password", dest="password", type=str, location="json", required=True, help="The user's password"
)
sign_up_parser.add_argument(
    "last_name", dest="last_name", location="json", required=False, type=str, help="The user's last_name"
)
sign_up_parser.add_argument(
    "first_name", dest="first_name", location="json", required=False, type=str, help="The user's first_name"
)
sign_up_parser.add_argument("email", dest="email", type=str, location="json", required=True, help="The user's email")


class SignUp(Resource):
    def post(self):
        args = sign_up_parser.parse_args()
        user = models.User.is_login_exist(args)
        if user:
            return {"message": "choose another login"}, HTTPStatus.CONFLICT
        models.User.create(args)
        return make_response(jsonify(message="user created successfully"), HTTPStatus.OK)
