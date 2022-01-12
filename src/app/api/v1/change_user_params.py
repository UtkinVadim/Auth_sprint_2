from http import HTTPStatus

from flask_jwt_extended import get_current_user, jwt_required
from flask_restful import Resource, reqparse

from app import models
from app.api.v1.exceptions import ChangeUserParamsException


user_params_parser = reqparse.RequestParser()
user_params_parser.add_argument(
    "login", dest="login", location="json", required=False, type=str, help="The user's login"
)
user_params_parser.add_argument(
    "old_password", dest="old_password", type=str, location="json", required=False, help="The user's password"
)
user_params_parser.add_argument(
    "new_password", dest="new_password", type=str, location="json", required=False, help="New user's password"
)


class ChangeUserParams(Resource):
    """
    Класс ручки для изменения параметров пользователя (логин+пароль)
    """

    @jwt_required()
    def post(self):
        args = user_params_parser.parse_args()
        user = get_current_user()
        try:
            self.check_args(user, args)
        except ChangeUserParamsException as e:
            return {"message": e.message}, e.status_code
        models.User.change_user(user.id, args)
        return {"message": "successfully changed"}, HTTPStatus.OK

    def check_args(self, user: models.User, args):
        if args.get("new_password"):
            self.check_passwords(user, args)
        if args.get("login"):
            if models.User.is_login_exist(args):
                raise ChangeUserParamsException(message="choose another login")

    @staticmethod
    def check_passwords(user: models.User, args: dict) -> None:
        old_password = args.get("old_password")
        if not old_password:
            raise ChangeUserParamsException(message="enter your old password", status_code=HTTPStatus.BAD_REQUEST)
        password_is_correct = user.check_password(old_password)
        if not password_is_correct:
            raise ChangeUserParamsException(message="invalid password", status_code=HTTPStatus.UNAUTHORIZED)
