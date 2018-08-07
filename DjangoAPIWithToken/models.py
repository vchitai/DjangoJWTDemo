from django.db import models

from DjangoAPIWithToken.managers import ClientManager


class ClientModel(models.Model):
    client_id = models.AutoField(primary_key=True)
    client_name = models.CharField(unique=True)
    password = models.CharField()

    objects = ClientManager()

    class Meta:
        db_table = 'client'
        managed = False
        app_label = 'client_auth'
