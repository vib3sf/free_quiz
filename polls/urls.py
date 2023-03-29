from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('create/', create_question, name='create'),
    path('question/<int:question_id>/<slug:question_slug>', show_question, name='show_question')
]
