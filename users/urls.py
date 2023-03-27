from django.urls import path
from .views import *

urlpatterns = [
    path('registration/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/<int:id>', profile, name='profile'),
]
