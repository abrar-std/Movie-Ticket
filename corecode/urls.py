from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('user_register', user_register, name='user_register'),
    path('movies', movies, name='movies'),
    path('user_login', user_login, name='user_login'),
    path('user_logout', user_logout, name='user_logout'),
    path('edit_profile/<uuid:pk>/', user_edit_profile.as_view(), name='user_edit_profile'),
]
