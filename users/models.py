# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import uuid
# Create your models here.

#_______________________________________________________________________________________________________________________

class User(models.Model):

    name = models.CharField(max_length=255 , null=False , blank=False)
    username = models.CharField(max_length=255 , null=False , blank=False , unique=True)
    password = models.CharField(max_length=255 , null=False , blank=False)
    email = models.CharField(max_length=555)
    contact_no = models.CharField(max_length=10)
    short_bio = models.CharField(max_length=555)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


#_______________________________________________________________________________________________________________________

class AccessToken(models.Model):
    user = models.ForeignKey(User)
    access_token = models.CharField(max_length=255)
    last_request_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def create_token(self):
        self.access_token = uuid.uuid4()


#_______________________________________________________________________________________________________________________

class Movie(models.Model):

    name = models.CharField(max_length=255)
    duration_in_minutes = models.IntegerField(default=120)
    release_date = models.DateTimeField()
    overall_rating = models.DecimalField(decimal_places=2 , max_digits= 4)
    censor_board_rating = models.CharField(max_length=5)
    poster_picture_url = models.CharField(max_length=255)
    user = models.ForeignKey(User)


#_______________________________________________________________________________________________________________________

class Genre(models.Model):

    name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


#_______________________________________________________________________________________________________________________

#Mapping table
class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie)
    genre = models.ForeignKey(Genre)


#_______________________________________________________________________________________________________________________

class MovieReview(models.Model):
    user = models.ForeignKey(User)
    movie = models.ForeignKey(Movie)
    rating = models.IntegerField(default=0)
    review = models.CharField(max_length=555)



