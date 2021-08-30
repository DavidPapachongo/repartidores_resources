from django.db import models
from django.db.models import Model

# Create your models here.

class RepartidoresModel(Model):
    activo = models.BooleanField()