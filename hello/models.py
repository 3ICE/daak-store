from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)


class Developer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Store(models.Model):
    pass


class Game(models.Model):
    game_name = models.CharField(max_length=255, unique=True)
    game_url = models.URLField()
    game_developer = models.ForeignKey(Developer)
    game_price = models.FloatField()
    game_copies_sold = models.PositiveIntegerField(default=0)


class Scores(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(User)

    score = models.PositiveIntegerField(default=0)
