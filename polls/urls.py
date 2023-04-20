from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('create_poll/', CreatePoll.as_view(), name='create_poll'),
    path('poll/<int:poll_id>/edit/', Edit.as_view(), name='edit'),
    path('poll/<int:poll_id>/', ShowPoll.as_view(), name='show_poll'),
    path('poll/<int:poll_id>/edit_poll/', EditPoll.as_view(), name='edit_poll'),
    path('poll/<int:poll_id>/delete_poll/', DeletePoll.as_view(), name='delete_poll'),
    path('poll/<int:poll_id>/create_question/', CreateQuestion.as_view(), name='create_question'),
    path('question/<int:question_id>/edit_question/', EditQuestion.as_view(), name='edit_question'),
    path('question/<int:question_id>/delete_question/', DeleteQuestion.as_view(), name='delete_question'),
    path('question/<int:question_id>/create_choice', CreateChoice.as_view(), name='create_choice'),
    path('choice/<int:choice_id>/edit_choice/', EditChoice.as_view(), name='edit_choice'),
    path('choice/<int:choice_id>/delete_choice/', DeleteChoice.as_view(), name='delete_choice'),
    path('poll/<int:poll_id>/vote/', VoteView.as_view(), name='show_vote'),
    path('poll/<int:poll_id>/vote', vote, name='vote'),
]
