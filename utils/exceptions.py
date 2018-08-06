from rest_framework import status
from rest_framework.exceptions import APIException


class BaseAPIException(APIException):
    def __init__(self, message=None, code=None):
        if message is None:
            message = self.default_detail
        if code is None:
            code = self.default_code

        self.detail = {
            'data': {},
            'error': {
                'message': message,
                'code': code,
            },
        }


class AuthenticationFailed(BaseAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Unauthorized'
    default_code = 'unauthorized'
