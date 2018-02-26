from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.IntegerField()
    wood = models.IntegerField()
    iron = models.IntegerField()
    crew = models.IntegerField()
    cannon = models.IntegerField()


class Activity(models.Model):
    pass


class Ship(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    crew = models.IntegerField()
    level = models.IntegerField()
    cannon = models.IntegerField()
    life = models.IntegerField()
    currentActivity = models.ForeignKey(Activity, on_delete=models.CASCADE)
