from django.urls import path, include, re_path
from .views import PollListCreateAPIView, PollDeleteAPIView, VoteListCreateAPIVIew

urlpatterns = [
    path('create/', PollListCreateAPIView.as_view(), name='api_create'),
    path('vote/', VoteListCreateAPIVIew.as_view(), name='api_vote'),
    path('delete/<int:pk>/', PollDeleteAPIView.as_view(), name='api_delete'),
    path('accounts/', include('rest_registration.api.urls'), name='api_accounts'),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
