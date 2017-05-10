"""amdb_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))

"""

from django.conf.urls import url
from django.contrib import admin
from users.views import create_user , get_user , login_user , create_movie , movie_list , movie_review #, logout
from django.conf.urls import include



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'user/create/' , create_user),
    url(r'^api-auth/' , include('rest_framework.urls' , namespace = 'rest_framework')),
    url(r'user/' , get_user),
    url(r'login/' , login_user) ,
    url(r'movie/create/' , create_movie) ,
    url(r'movie/list/' , movie_list) ,
    url(r'movie/review/' , movie_review)
#    url(r'logout/' , logout)


]
