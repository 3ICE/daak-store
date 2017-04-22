from django.db import models
from django.contrib.auth.models import *

class Player(models.Model):
    developer = models.BooleanField(default=False)
    # player is not necessary, simply check if not developer
    activated = models.BooleanField(default=False) # 3ICE: Can't remove...
    user = models.OneToOneField(User)

    def method_example(self):
        pass

class Game(models.Model):
    game_name = models.CharField(max_length=255, unique=True)
    game_url = models.URLField()
    game_developer = models.ForeignKey(User)
    game_price = models.FloatField()
    game_copies_sold = models.PositiveIntegerField(default=0)


class Score(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(User)
    score = models.PositiveIntegerField(default=0)
    state = models.TextField(blank=True, null=True)
