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
        fields = ('game_name', )

class ScoreSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Score
		fields = ('score', )

class ScoresSerializer(serializers.ModelSerializer):
    players = UserSerializer(many=True)
    scores = ScoresSerializer(many=True)
    game = GameSerializer()
    class Meta:
        model = Score
        fields = ('game', 'player', 'score')

