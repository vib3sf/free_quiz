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
            'class': 'form-control',
            'placeholder': 'Enter choice text'
        }


ChoiceFormSet = forms.formset_factory(ChoiceAddForm, extra=2)
