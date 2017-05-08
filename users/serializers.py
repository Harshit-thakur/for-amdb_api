from rest_framework.serializers import ModelSerializer
from models import User , Movie


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'name' , 'username' , 'short_bio' , 'created_on' , 'updated_on' , 'email')


class MovieSerializer(ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id', 'name', 'duration_in_minutes', 'release_date',
                  'overall_rating', 'censor_board_rating', 'poster_picture_url')

class Movielist(ModelSerializer):

    class Meta:
        model = Movie
        fields = ('name')