from http import HTTPStatus

from flask_restful import Resource, reqparse

from app import models
from app.jwt import jwt_with_role_required


role_parser = reqparse.RequestParser()
role_parser.add_argument("title", dest="title", type=str, location="json", required=True, help="The role's title")

role_editor_parser = reqparse.RequestParser()
role_editor_parser.add_argument(
    "title", dest="title", type=str, location="json", required=True, help="The role's current title"
)
role_editor_parser.add_argument(
    "new_title", dest="new_title", type=str, location="json", required=True, help="The role's new title"
)


class Role(Resource):
    @jwt_with_role_required("admin")
    def post(self):
        args = role_parser.parse_args()
        if models.Role.is_role_exist(args):
            return {"message": "role already exists"}, HTTPStatus.CONFLICT
        models.Role.create(**args)
        return {"message": "role created"}, HTTPStatus.CREATED

    @jwt_with_role_required("admin")
    def get(self):
        roles = models.Role.get_all()
        return {"roles": roles}, HTTPStatus.OK

    @jwt_with_role_required("admin")
    def delete(self):
        args = role_parser.parse_args()
        title = args["title"]
        role = models.Role.query.filter_by(title=title).one_or_none()
        if not role:
            return {"message": "role does not exist"}, HTTPStatus.CONFLICT
        models.Role.delete(role)
        return {"message": "role deleted"}, HTTPStatus.OK

    @jwt_with_role_required("admin")
    def patch(self):
        args = role_editor_parser.parse_args()
        role = models.Role.is_role_exist(args)
        if not role:
            return {"message": "role does not exist"}, HTTPStatus.CONFLICT
        models.Role.update(args)
        return {"message": "role updated"}, HTTPStatus.OK
