from django.db import models
import datetime

from django.db import models
from django.utils import timezone


class Carro(models.Model):
    carro_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("fecha de publicación")

    def __str__(self):
        return self.carro_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Caracteristica(models.Model):
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE)
    caracteristica_text = models.CharField(max_length=200)

    def __str__(self):
        return self.caracteristica_text