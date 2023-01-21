from django.db import models

# Create your models here.


class ClientContainer(models.Model):
    container = models.CharField(max_length=11,)
    client_name = models.CharField(max_length=30)
    date = models.DateField()

