from django.contrib.gis.db import models

class State(models.Model):
    name = models.CharField(max_length=100)
    geom = models.MultiPolygonField(srid=4326,null=True, blank=True)

from django.contrib.gis.db import models

class District(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    geom = models.MultiPolygonField(null=True, blank=True)  # ✅ Fix here

class Taluka(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    geom = models.MultiPolygonField(null=True, blank=True)  # ✅ Fix here too


class Village(models.Model):
    name = models.CharField(max_length=100)
    taluka = models.ForeignKey(Taluka, on_delete=models.CASCADE)
    geom = models.MultiPolygonField(srid=4326)
    data = models.JSONField(null=True, blank=True)
    population = models.IntegerField(null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)


class Mahamarg(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    geom = models.MultiLineStringField(srid=4326)
