from datetime import timedelta, datetime

from django.utils.translation import ugettext as _
from django.utils.encoding import smart_text
from jose import jwt
from django.conf.global_settings import SECRET_KEY
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

EXP_DATE = timedelta(seconds=300)


def get_jwt_token(client_info):
    payload = {
        'client_id': client_info.client_id,
        'client_name': client_info.client_name,
        'exp': datetime.utcnow() + EXP_DATE
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def validate_jwt_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])


def get_jwt_value(request):
    auth = get_authorization_header(request).split()

    if len(auth) == 0:
        msg = _('Invalid Authorization header. No credentials provided.')
        raise AuthenticationFailed(msg)
    elif len(auth) > 2:
        msg = _('Invalid Authorization header. Credentials string '
                'should not contain spaces.')
        raise AuthenticationFailed(msg)

    return auth[0]
