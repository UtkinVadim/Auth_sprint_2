from http import HTTPStatus

from flask_restful import Resource, reqparse

from app import models
from app.jwt import jwt_with_role_required

role_parser = reqparse.RequestParser()
role_parser.add_argument("user_id", dest="user_id", location="json", required=True, type=str, help="user_id")
role_parser.add_argument("role_id", dest="role_id", location="json", required=True, type=str, help="role_id")


class RoleManipulation(Resource):
    """
    Класс ручки для добавления или удаления роли пользователю

    """

    @jwt_with_role_required("admin")
    def post(self):
        args = role_parser.parse_args()
        if models.UserRole.is_user_role_exists(args):
            return {"message": "user already has role"}, HTTPStatus.CONFLICT
        models.UserRole.add(args["user_id"], args["role_id"])
        return {"message": "role added"}, HTTPStatus.OK

    @jwt_with_role_required("admin")
    def delete(self):
        args = role_parser.parse_args()
        if not models.UserRole.is_user_role_exists(args):
            return {"message": "user has no role"}, HTTPStatus.CONFLICT
        models.UserRole.delete(args["user_id"], args["role_id"])
        return {"message": "role deleted"}, HTTPStatus.OK
