from rest_framework import serializers
from .models import Movie, Rating
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model=Movie
        fields = ('id', 'title', 'description', 'no_of_rating', 'avg_rating')

class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model=Rating
        fields = ('id', 'stars', 'user', 'movie')
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id', 'username', 'password')
        #damit kann man das password nicht gezeigt
        extra_kwargs={'password': {'write_only': True, 'required': True}}


    def create(self, validated_data):
        user= User.objects.create_user(**validated_data)
        #create token für jeden user
        Token.objects.create(user=user)
        return user
