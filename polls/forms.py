from django import forms
from .models import *


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['title', 'description', 'can_revote']
        widgets = {
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']
        widgets = {
        }


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
        widgets = {
            'class': 'form-control',
            'placeholder': 'Enter choice text'
        }
