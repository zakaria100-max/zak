from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Movie, Rating
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from .serializers import MovieSerializer, RatingSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated

class MovieViewSet(viewsets.ModelViewSet):
    queryset= Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes=(TokenAuthentication,)
    permission_classes=(IsAuthenticated,)


    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:
            movie=Movie.objects.get(id=pk)
            stars=request.data['stars']
            user= request.user

            #user= User.objects.get(id=1)
            print("my user", user.username)

            try:
                rating =Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars=stars
                rating.save()
                serializer= RatingSerializer(rating, many=False)

                print("test",movie.title)
                response= {"messages": 'Rating update', 'Ergbins':serializer.data }
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating =Rating.objects.create(user=user.id, movie=movie.id, stars=stars)
                serializer= RatingSerializer(rating, many=False)

                print("test",movie.title)
                response= {"messages": 'Rating created', 'Ergbins':serializer.data }
                return Response(response, status=status.HTTP_200_OK)

            print("test",movie.title)
            response= {"messages": 'WILLKOMMEN' }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response= {"messages": 'NOT WORK' }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)



class RatingViewSet(viewsets.ModelViewSet):
    queryset= Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes=(TokenAuthentication,)
    permission_classes=(IsAuthenticated,) # oder AllowyAny auch import oben


class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class= UserSerializer
