from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('create_poll/',CreatePoll.as_view(), name='create_poll'),
    path('edit_poll/<int:poll_id>',EditPoll.as_view(), name='edit_poll'),
    path('delete_poll/<int:poll_id>',DeletePoll.as_view(), name='delete_poll'),
    path('poll/<int:poll_id>/',ShowPoll.as_view(), name='show_poll'),
    path('create_question/<int:poll_id>',CreateQuestion.as_view(), name='create_question'),
    path('edit_question/<int:question_id>/',EditQuestion.as_view(), name='edit_question'),
    path('delete_question/<int:question_id>/',DeleteQuestion.as_view(), name='delete_question'),
    path('create_choice/<int:question_id>/',CreateChoice.as_view(), name='create_choice'),
    path('edit_choice/<int:choice_id>/',EditChoice.as_view(), name='edit_choice'),
    path('delete_choice/<int:choice_id>/',DeleteChoice.as_view(), name='delete_choice'),
    path('vote/<int:choice_id>/', vote, name='vote'),
]
