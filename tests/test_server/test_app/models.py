from django.db import models


class DummyModel(models.Model):
    dummy_int = models.IntegerField(null=True, blank=True)
