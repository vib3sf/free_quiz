from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('create_poll/', create_poll, name='create_poll'),
    path('poll/<int:poll_id>/', login_required(ShowPoll.as_view()), name='show_poll'),
    path('create_question/<int:poll_id>', login_required(CreateQuestion.as_view()), name='create_question'),
    path('edit_question/<int:question_id>/', edit_question, name='edit_question'),
    path('delete_question/<int:question_id>/', delete_question, name='delete_question'),
    path('create_choice/<int:question_id>/', add_choice, name='create_choice'),
    path('edit_choice/<int:choice_id>/', edit_choice, name='edit_choice'),
    path('delete_choice/<int:choice_id>/', delete_choice, name='delete_choice'),
    path('vote/<int:choice_id>/', vote, name='vote'),
]
