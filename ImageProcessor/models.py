from django.db import models


class RawImageModel(models.Model):
    floor_plan = models.ImageField()


class ProcessedImageModel(models.Model):
    floor_plan = models.ImageField()
    area = models.IntegerField()
    compartments = models.IntegerField()
    windows = models.IntegerField()
    doors = models.IntegerField()
