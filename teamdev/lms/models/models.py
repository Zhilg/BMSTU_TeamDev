from django.db import models

class Tasks(models.Model):
    filename = models.CharField(max_length=100, unique=True)
    theme = models.CharField(max_length=100)
