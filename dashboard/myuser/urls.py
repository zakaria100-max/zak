
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import MovieViewSet,RatingViewSet, UserViewSet


router = routers.DefaultRouter()
router.register('movies', MovieViewSet)
router.register('rating', RatingViewSet)
router.register('users', UserViewSet)


urlpatterns = [

    path('meinapis/', include(router.urls)),

 ]
