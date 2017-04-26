from rest_framework import serializers 
from hello.models import * 

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Player
        fields = ('username', )

class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('game_name', 'game_url', 'game_developer', 'game_price', 'game_sales' )

class ScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Score
        fields = ('score', )

class ScoresSerializer(serializers.ModelSerializer):
    players = UserSerializer(many=True)
    scores = ScoreSerializer(many=True)
    game = GameSerializer(many=True)
    class Meta:
        model = Score
        fields = ('game', 'players', 'player', 'score')
