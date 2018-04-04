from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.IntegerField(validators=[MinValueValidator(0)])
    wood = models.IntegerField(validators=[MinValueValidator(0)])
    iron = models.IntegerField(validators=[MinValueValidator(0)])
    crew = models.IntegerField(validators=[MinValueValidator(0)])
    cannons = models.IntegerField(validators=[MinValueValidator(0)])


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
    crew = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    level = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    cannon = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    life = models.IntegerField(default=100, validators=[MinValueValidator(0)])
    currentActivity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True)
    endActivity = models.DateTimeField(null=True)
    xp = models.IntegerField(default=0)
