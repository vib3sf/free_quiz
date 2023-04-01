from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('create/', create_question, name='create'),
    path('htmx/create_choice_form', add_choice, name='create_choice'),
    path('question/<int:question_id>/', show_question, name='show_question'),
    path('create_choice/<int:question_id>', add_choice, name='create_choice'),
    path('delete_choice/<int:choice_id>', delete_choice, name='delete_choice'),
    path('edit/<int:choice_id>', edit_choice, name='edit_choice')
]
