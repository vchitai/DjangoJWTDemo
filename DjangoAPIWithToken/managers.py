from django.db import models
from django.contrib.auth.hashers import make_password, check_password



class ClientManager(models.Manager):
    def create_new_client(self,client_name, password):
        new_client = {
            'client_name': client_name,
            'password': make_password(password)
        }
        super(ClientManager, self).create(**new_client)

    def authenticate_client(self, client_name, password):
        client = super(ClientManager, self).filter(client_name=client_name).first()
        if client is None or not check_password(password, client.password):
            return None
        return client