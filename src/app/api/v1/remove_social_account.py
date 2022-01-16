from http import HTTPStatus

from flask_restful import Resource, reqparse
from flask_jwt_extended import get_current_user, jwt_required

from app.models import SocialAccount

remove_social_account = reqparse.RequestParser()
remove_social_account.add_argument(
    "social_name", dest="social_name", location="json", required=True, type=str, help="Name of social service."
)


class RemoveSocialAccount(Resource):
    """
    Класс ручки для открепления соц сервиса от аккаунта.
    """

    @jwt_required()
    def post(self):
        social_name = remove_social_account.parse_args().get("social_name")
        user = get_current_user()
        social_account = SocialAccount.query.filter_by(user_id=user.id, social_name=social_name).one_or_none()
        if not social_account:
            return {"message": "no social account"}, HTTPStatus.CONFLICT
        social_account.delete()
        return HTTPStatus.OK
