# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework.decorators import api_view

from rest_framework.response import Response

from django.http import HttpResponse

from users.models import User

from users.models import AccessToken

from users.models import Movie, Genre, MovieGenre , MovieReview

from users.serializers import UserSerializer , MovieSerializer , Movielist

from django.contrib.auth.hashers import make_password ,check_password

from datetime import datetime

from django.http import HttpResponse


# Create your views here.
#_______________________________________________________________________________________________________________________
@api_view(['POST'])
def create_user(request):
    # For accessing post data
    print request.data
    name = request.data["name"]
    username = request.data["username"]
    password = request.data["password"]
    email = request.data["email"]
    short_bio = request.data["short_bio"]
    contact_no = request.data["contact_no"]

    if name is None or len(name) == 0:
        return Response({"Error message": "name field can't be empty"} , status = 400)

    if password is None or len(password) < 6:
        return Response({"Error message": "password field can't be less than 6"}, status=400)

    does_usename_exist = User.objects.filter(username = username).first()

#    print does_usename_exist

    if does_usename_exist is not None:
        return Response({"Error message": "Username already Exist. please try another"} , status = 400)


    new_user = User(name = name , username = username , password = make_password(password) ,email = email , short_bio = short_bio , contact_no = contact_no)

    new_user.save()

    return Response(UserSerializer(instance = new_user).data , status = 200)

   # return Response({"Success": "User_created"} , status = 200)

  #  print name , username , password , short_bio

 #   return HttpResponse(True)


#________________________________________________________________________________________________________________________

@api_view(["GET"])
def get_user(request):
   # print request.query_params  # for get Data
  #  return HttpResponse(True)

    if "user_id" in request.query_params:
     #   print "User id found in query params"
        user = User.objects.filter(id = request.query_params['user_id'])
        print user
        if len(user) > 0:
            return Response(UserSerializer(instance=user[0]).data, status=200)
         #   print "user was found"
        else:
            return Response({"message": "user not found"}, status=200)

            #  print "user not found"

    else:
        users = User.objects.all()

        return Response(UserSerializer(instance = users , many = True).data , status = 200)

       # print "User id not found !"
     #   print request.query_params


   # return HttpResponse(True)

#_______________________________________________________________________________________________________________________


@api_view(['POST'])
def login_user(request):

    username = None
    password = None

    if "username" in request.data:
        username = request.data["username"]


    if "password" in request.data:
        password = request.data["password"]


    if not username or not password:
        return Response({"message": "Either username or password is invalid"} , status = 200)



    user = User.objects.filter(username = username).first()

    if user:
        if not check_password(password , user.password):
            return Response({"message": "Either username or password is invalid"} , status = 200)
        else:
            token = AccessToken(user = user)
            token.create_token()
            token.save()
            return Response({"token": token.access_token} , status = 200)


    else:
        return Response({"message": "Either username or password is invalid"} , status = 200)

def check_token(request):
    access_token = request.META['HTTP_TOKEN']
    token_exists = AccessToken.objects.filter(access_token=access_token, is_valid=True).first()

    if token_exists:
        return token_exists.user

    else:
        return None


#_______________________________________________________________________________________________________________________

@api_view(["POST"])
def create_movie(request):

    current_user = check_token(request)

    if current_user:
        print current_user.name
        name = request.data['name']
        duration_in_minutes = request.data["duration_in_minutes"]
        release_date = datetime.strptime(request.data['release_date'], '%Y-%m-%d')
        censor_board_rating = request.data['censor_board_rating']
        poster_picture_url = request.data['poster_picture_url']
        genre_ids = request.data['genre_id']

        if len(name) == 0:
            return Response({"message": "Name cannot be empty!"}, status=200)

        # Collect all the genre objects
        genres = []

        for id in genre_ids:

            genre = Genre.objects.filter(id=id).first()
            if not genre:
                return Response({"message": "Invalid genre id! This genre does not exist"}, status = 200)
            else:
                genres.append(genre)

        if duration_in_minutes <= 0:
            return Response({"message": "Duration is invalid. A movie cannot be zero or less minutes long"}, status=200)

        new_movie = Movie(name=name, duration_in_minutes=duration_in_minutes,
                          release_date=release_date, censor_board_rating=censor_board_rating,
                          poster_picture_url=poster_picture_url, user=current_user)
        new_movie.save()

        for genre in genres:
            MovieGenre.objects.create(movie=new_movie, genre=genre)

        return Response(MovieSerializer(instance=new_movie).data, status=200)

    else:

        return Response({"message": "you are not authorized to perform this action"}, status=400)





"""
    access_token = request.META['HTTP_TOKEN']
    token_exists = AccessToken.objects.filter(access_token = access_token , is_valid = True).first()

    if not token_exists:
        return Response({"message": "You are not authorized to perform this action"} , status = 400)
    else:
        current_user = token_exists.user
        return Response("Hi %s " % (current_user.username), status = 200)





def check_token(token):

    token = AccessToken.objects.filter(token = token)

    if token:
        return token.user
    else:
        return None

"""

#_______________________________________________________________________________________________________________________

@api_view(["GET"])
def movie_list(request):
    if "q" in request.query_params:
     #   print "query parameter q found in query params"
        movie = Movie.objects.filter(name = request.query_params['q'])
        print movie
        if len(movie) > 0:
            return Response(movie , status=200)
            #   print "founded movie name"
        else:
             return Response({"message": "movie not found"}, status=200)
            #  print "movie not found"

    else:
        movies = Movie.objects.all()

        return Response(Movielist(instance = movies, many = True).data, status = 200)





        #   current_user = check_token(request)
#_______________________________________________________________________________________________________________________

@api_view(["POST"])
def movie_review(request):
    if not AccessToken.is_valid:
        #checking acccesstoken validation
       return Response({"message":"invalid access token"} , status = 400)
    else:
        current_user = check_token(request)
        user = current_user
        movie = request.data["movie"]
        rating = request.data["rating"]
        review = request.data["review"]

        if rating > 5 or rating <0:
            return Response({"message": "Rating can't be greater than 5" }, status = 200)

        does_user_already_reviewed = MovieReview.objects.filter(user=user).first()
       #print does_user_already_reviewed

        if does_user_already_reviewed is not None:
            return Response({"Error message": "Username already reviewed the movie. please try another"}, status=400)

        new_review = MovieReview(user = user , movie = movie , rating = rating , review = review)
        new_review.save()
        return Response({"message": "successfully reviewed"})



#_______________________________________________________________________________________________________________________
@api_view(["POST"])
def logout(request):
    current_user = check_token(request)
    if current_user:
        print current_user.name


