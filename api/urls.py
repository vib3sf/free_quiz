from django.urls import path, include, re_path
from .views import PollListCreateAPIView, PollDeleteAPIView, VoteCreateAPIVIew

urlpatterns = [
    path('polls/', PollListCreateAPIView.as_view()),
    path('polls/<int:poll_id>/', PollListCreateAPIView.as_view()),
    path('vote/', VoteCreateAPIVIew.as_view()),
    path('delete/<int:pk>/', PollDeleteAPIView.as_view()),
    path('accounts/', include('rest_registration.api.urls')),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
