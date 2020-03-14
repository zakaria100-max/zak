from django.db import models

# Create your models here.
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

from .constants import TITLE_CHOICES, ROLE_CHOICES, SALUTATION_CHOICES
# Create your models here.

class Benutzer(models.Model):

    email = models.EmailField(('Email'), unique=True)
    first_name = models.CharField(('First Name'), max_length=64)
    last_name = models.CharField(('Last Name'), max_length=64)
    role = models.CharField(
        ('Role'), max_length=20, choices=ROLE_CHOICES, null=True, blank=True)
    is_active = models.BooleanField(('Is Active'), default=False)
    is_admin = models.BooleanField(('Is Admin'), default=False)
    is_staff = models.BooleanField(('Is Staff'), default=False)
    email_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(('Date joined'), auto_now_add=True)

    title = models.CharField(
        ('Title'), max_length=10, choices=TITLE_CHOICES, null=True, blank=True)

    no_password_set = models.BooleanField(
        ('No password set'), default=False,
        help_text=('Forces to change password on login'))
    jahr = models.IntegerField(default=0)
    adresse= models.CharField(max_length =200)
    #status = models.CharField(max_length=1, choices=STATUS_CHOICES)



    class Meta:
        verbose_name = ('Email user')
        verbose_name_plural = ('Benutzer')

class Author(models.Model):
    name=models.CharField(max_length=200)
    geburtsdatum=models.DateTimeField(auto_now_add=True)

class Book(models.Model):
    title= models.CharField(max_length=100)
    author=models.ForeignKey(Author , on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title

class Movie(models.Model):
    title = models.CharField(max_length=32)
    description= models.TextField(max_length=300)

    def no_of_rating(self):
        ratings= Rating.objects.filter(movie=self)
        return len(ratings)

    def avg_rating(self):

        sum=0
        ratings= Rating.objects.filter(movie=self)
        for rating in ratings:
            sum+=rating.stars
            if len(ratings)>0:
                return sum/len(ratings)
            else:
                return 0


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together= (('user', 'movie'),)
        index_together = (('user', 'movie'),)
