from django.db import models


class RawImageModel(models.Model):
    floor_plan = models.ImageField()

    def __unicode__(self):
        return u"photo {0}".format(self.floor_plan)


class ProcessedImageModel(models.Model):
    floor_plan = models.ImageField()
    area = models.IntegerField(default=58)
    compartments = models.IntegerField(default=7)
    windows = models.IntegerField(default=5)
    doors = models.IntegerField(default=8)
