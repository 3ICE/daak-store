from rest_framework import serializers 
from hello.models import * 

class ScoreSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Score
		fields = ('score', )