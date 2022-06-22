from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=128, default="")
    def __str__(self) :
        return self.name

class State(models.Model):
    name = models.CharField(max_length=128, default="")
    def __str__(self) :
        return self.name

class Iso(models.Model):
    name = models.CharField(max_length=128, default="")
    def __str__(self) :
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=128, default="")
    def __str__(self) :
        return self.name

#Here comes the through table.
# Some columns are of real interest as tables than need relationships
# the other are gonna stand as "metadata" in the through table which are
# name, year, latitude, longitude, justification, area_hectares.

class Site(models.Model):
    name = models.CharField(max_length=300)
    year = models.IntegerField(null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    description = models.TextField(null=True)
    justification = models.TextField(null=True)
    area_hectares = models.FloatField(null=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True)
    region = models.ForeignKey("Region", on_delete=models.CASCADE, null=True)
    iso = models.ForeignKey("Iso", on_delete=models.CASCADE, null=True)
    state = models.ForeignKey("State", on_delete=models.CASCADE, null=True)

    def __str__(self) :
        return self.name
