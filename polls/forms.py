from django import forms
from .models import *


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['title', 'description', 'can_revote']
        widgets = {
        }
