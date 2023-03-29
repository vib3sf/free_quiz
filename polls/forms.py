from django import forms
from .models import *


class QuestionAddForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['question_text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 20}),
        }


class ChoiceAddForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
        widgets = {
            'choice_text': forms.TextInput(attrs={'class': 'form-control', })
        }
