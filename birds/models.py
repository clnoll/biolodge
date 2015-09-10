from django.db import models


class Location(models.Model):

    name = models.CharField(null=False, unique=True)
    polygon = models.TextField()


class Subspecies(models.Model):

    order = models.CharField()
    family = models.CharField()
    genus = models.CharField()
    species = models.CharField()
    subspecies = models.CharField()
    raw_location = models.TextField()
    ebird_id = models.CharField(unique=True)
    common_name = models.CharField()

    locations = models.ManyToManyField(Location)
