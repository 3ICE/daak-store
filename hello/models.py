from django.db import models
from django.contrib.auth.models import *


#contains player information
class Player(models.Model):
    developer = models.BooleanField(default=False)
    # player is not necessary, simply check if not developer
    activated = models.BooleanField(default=False) # 3ICE: Can't remove...
    user = models.OneToOneField(User)

    def method_example(self):
        pass
#contains information aout game
class Game(models.Model):
    game_name = models.CharField(max_length=255)
    game_url = models.URLField()
    game_developer = models.ForeignKey(User)
    game_price = models.PositiveIntegerField(default=0)
    game_sales = models.PositiveIntegerField(default=0)

#stores game score and player name and game name
class Score(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(User)
    score = models.PositiveIntegerField(default=0)
    state = models.TextField(blank=True, null=True)
