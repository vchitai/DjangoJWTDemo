from django.contrib.auth.models import User
from jose.exceptions import ExpiredSignatureError, JWTError, JWTClaimsError
from rest_framework.authentication import BaseAuthentication

from django.utils.translation import ugettext as _
from rest_framework.exceptions import AuthenticationFailed

from DjangoAPIWithToken.models import ClientModel
from utils.jwt import get_jwt_value, validate_jwt_token


class MyJSONWebTokenAuthentication(BaseAuthentication):
    """
    Token based authentication using the JSON Web Token standard.
    """

    www_authenticate_realm = 'api'

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return '{0} realm="{1}"'.format("Jwt", self.www_authenticate_realm)

    def authenticate(self, request):
        """
        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication.  Otherwise returns `None`.
        """
        jwt_value = get_jwt_value(request)
        if jwt_value is None:
            return None
        try:
            payload = validate_jwt_token(jwt_value)
        except ExpiredSignatureError:
            msg = _('Signature has expired.')
            raise AuthenticationFailed(msg)
        except JWTClaimsError:
            raise AuthenticationFailed()
        except JWTError:
            msg = _('Error decoding signature.')
            raise AuthenticationFailed(msg)

        client = self.authenticate_credentials(payload)
        client_name = client['client_name']
        try:
            user = User.objects.get(username=client_name)
        except User.DoesNotExist:
            # Create a new user. There's no need to set a password
            # because only the password from settings.py is checked.
            user = User(username=client_name)
            user.save()

        return user, client

    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id and email.
        """
        client_name = payload['client_name']
        if not client_name:
            msg = _('Invalid payload.')
            raise AuthenticationFailed(msg)

        client = ClientModel.objects.filter(client_name=client_name).first()
        if client is None:
            msg = _('Invalid signature.')
            raise AuthenticationFailed(msg)
        return payload
        # User = get_user_model()
        # username = jwt_get_username_from_payload(payload)
        #
        # if not username:
        #     msg = _('Invalid payload.')
        #     raise exceptions.AuthenticationFailed(msg)
        #
        # try:
        #     user = User.objects.get_by_natural_key(username)
        # except User.DoesNotExist:
        #     msg = _('Invalid signature.')
        #     raise exceptions.AuthenticationFailed(msg)
        #
        # if not user.is_active:
        #     msg = _('User account is disabled.')
        #     raise exceptions.AuthenticationFailed(msg)
        #
        # return user
