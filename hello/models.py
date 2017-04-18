from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    game_name = models.CharField(max_length=255, unique=True)
    game_url = models.URLField()
    game_developer = models.ForeignKey(User)
    game_price = models.FloatField()
    game_copies_sold = models.PositiveIntegerField(default=0)


class Scores(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(User)

    score = models.PositiveIntegerField(default=0)
