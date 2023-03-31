from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('create/', create_question, name='create'),
    path('htmx/create_choice_form', create_choice, name='create_choice'),
    path('question/<int:question_id>/<slug:question_slug>', show_question, name='show_question'),
    path('create_choice/<int:question_id>', create_choice, name='create_choice')
]
