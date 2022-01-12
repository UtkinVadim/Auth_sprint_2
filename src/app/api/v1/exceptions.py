from http import HTTPStatus


class ChangeUserParamsException(Exception):
    def __init__(self, message: str, status_code=HTTPStatus.CONFLICT):
        self.message = message
        self.status_code = status_code
