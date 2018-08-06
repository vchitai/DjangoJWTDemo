from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext as _
from rest_framework import serializers

from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.compat import get_username_field, PasswordField

from DjangoAPIWithToken.models import ClientModel
from utils.jwt import get_jwt_token


class Serializer(serializers.Serializer):
    @property
    def object(self):
        return self.validated_data


class JWTTokenProviderSerializer(Serializer):
    client_name = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        credentials = {
            'client_name': attrs.get('client_name'),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            client = ClientModel.objects.authenticate_client(credentials['client_name'], credentials['password'])

            if client is not None:
                ### Start Authenticate User

                # if not user.is_active:
                #     msg = _('User account is disabled.')
                #     raise serializers.ValidationError(msg)

                payload = get_jwt_token(client)

                ### Return JWT Token
                return {
                    'token': payload,
                    'client': client.client_name
                }
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)
