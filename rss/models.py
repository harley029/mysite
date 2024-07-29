from django.db import models


class News(models.Model):

    title = models.CharField(max_length=512)
    link = models.CharField(max_length=512, default="", unique=True)
    description = models.CharField(max_length=512, default="", blank=True, null=True)
