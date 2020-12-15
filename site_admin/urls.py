from django.urls import path
from .views import *
urlpatterns = [
    path('', admin_login, name='admin_login'),
    path('admin_logout', admin_logout, name='admin_logout'),
    path('admin_dashboard', admin_dashboard, name='admin_dashboard'),
    path('manage_users', admin_manage_users, name='admin_manage_users'),
    path('search_users', admin_search_users, name='admin_search_users'),
    ]
