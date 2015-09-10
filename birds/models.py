from django.db import models


class Location(models.Model):

    name = models.CharField(null=False, unique=True, max_length=50)
    polygon = models.TextField()


class Subspecies(models.Model):

    order = models.CharField(max_length=50)
    family = models.CharField(max_length=50)
    genus = models.CharField(max_length=50)
    species = models.CharField(max_length=50)
    subspecies = models.CharField(max_length=50)
    raw_location = models.TextField()
    ebird_id = models.CharField(unique=True, max_length=50)
    common_name = models.CharField(max_length=50)

    locations = models.ManyToManyField(Location)
