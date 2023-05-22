from django.urls import path
from .views import PollCreateAPIView

urlpatterns = [
    path('create/', PollCreateAPIView.as_view(), name='api_create'),
]
