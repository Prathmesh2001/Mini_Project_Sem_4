from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class CarDetails(models.Model):
    car_age = models.IntegerField()
    km_driven = models.IntegerField()
    mileage = models.FloatField()
    horsepower = models.FloatField()
    price = models.FloatField()

