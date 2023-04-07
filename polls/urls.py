from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('create_poll/', login_required(CreatePoll.as_view()), name='create_poll'),
    path('edit_poll/<int:poll_id>', login_required(EditPoll.as_view()), name='edit_poll'),
    path('delete_poll/<int:poll_id>', login_required(DeletePoll.as_view()), name='delete_poll'),
    path('poll/<int:poll_id>/', login_required(ShowPoll.as_view()), name='show_poll'),
    path('create_question/<int:poll_id>', login_required(CreateQuestion.as_view()), name='create_question'),
    path('edit_question/<int:question_id>/', login_required(EditQuestion.as_view()), name='edit_question'),
    path('delete_question/<int:question_id>/', login_required(DeleteQuestion.as_view()), name='delete_question'),
    path('create_choice/<int:question_id>/', login_required(CreateChoice.as_view()), name='create_choice'),
    path('edit_choice/<int:choice_id>/', login_required(EditChoice.as_view()), name='edit_choice'),
    path('delete_choice/<int:choice_id>/', login_required(DeleteChoice.as_view()), name='delete_choice'),
    path('vote/<int:choice_id>/', vote, name='vote'),
]
