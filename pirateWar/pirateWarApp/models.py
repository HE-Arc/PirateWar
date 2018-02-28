from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.IntegerField()
    wood = models.IntegerField()
    iron = models.IntegerField()
    crew = models.IntegerField()
    cannons = models.IntegerField()


class Category(models.Model):
    name = models.CharField(max_length=50)


class Activity(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    rewardGold = models.IntegerField()
    rewardWood = models.IntegerField()
    rewardIron = models.IntegerField()
    level = models.IntegerField()
    duration = models.DurationField()


class Ship(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    crew = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    cannon = models.IntegerField(default=0)
    life = models.IntegerField(default=100)
    # currentActivity = models.ForeignKey(Activity, on_delete=models.CASCADE, default=0)
