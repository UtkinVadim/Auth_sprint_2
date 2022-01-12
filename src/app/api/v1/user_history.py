from http import HTTPStatus

from flask import jsonify, make_response
from flask_jwt_extended import get_current_user, jwt_required
from flask_restful import Resource

from app import models


class UserHistory(Resource):
    """
    Класс для ручки со списком логонов (успешных сеансов аутентификации) пользователя.

    """

    @jwt_required()
    def get(self):
        user = get_current_user()
        events = models.LoginHistory.get_user_events(user_id=user.id)
        return make_response(jsonify(events=events), HTTPStatus.OK)
