from django.urls import path
from .views import PollListCreateAPIView, PollDeleteAPIView

urlpatterns = [
    path('create/', PollListCreateAPIView.as_view(), name='api_create'),
    path('delete/<int:pk>', PollDeleteAPIView.as_view(), name='api_delete'),
]
