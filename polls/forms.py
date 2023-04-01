from django import forms
from .models import *


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
