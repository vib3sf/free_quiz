from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import *

urlpatterns = [
    path('registration/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', Profile.as_view(), name='profile'),
]
