from django.urls import path, include
from .views import PollListCreateAPIView, PollDeleteAPIView

urlpatterns = [
    path('create/', PollListCreateAPIView.as_view(), name='api_create'),
    path('delete/<int:pk>', PollDeleteAPIView.as_view(), name='api_delete'),
    path('accounts/', include('rest_registration.api.urls'), name='accounts'),
]
