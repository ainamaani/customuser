from django.urls import path
from . import views

urlpatterns=[
    path('register_user/', views.register_user, name='register'),
    path('fetch_users/', views.fetch_all_users, name='users'),
    path('login_user/', views.user_login, name='login'),
    path('logout_user/', views.user_logout, name='logout')
]