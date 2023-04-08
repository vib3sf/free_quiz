from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('registration/', Register.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', login_required(Profile.as_view()), name='profile'),
]
