from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('create_poll/', CreatePoll.as_view(), name='create_poll'),
    path('poll/<int:poll_id>/', ShowPoll.as_view(), name='show_poll'),
    path('poll/<int:poll_id>/vote/', Pick.as_view(), name='show_vote'),
    path('poll/<int:poll_id>/vote', vote, name='vote'),
    path('create/', create, name='create'),
]
