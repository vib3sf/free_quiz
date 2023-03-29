from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *


def index(request):
    return render(request, "polls/home.html")


@login_required
def create_question(request):
    choice_form_set = formset_factory(ChoiceAddForm, extra=2)
    if request.method == 'POST':
        formset = choice_form_set(request.POST)
        question_form = QuestionAddForm(request.POST)
        if question_form.is_valid() and formset.is_valid():
            question = question_form.save(commit=False)
            question.creator_id = request.user.id
            question.save()
            for form in formset:
                if form.cleaned_data:
                    choice = form.save(commit=False)
                    choice.question_id = question.id
                    choice.save()
            return redirect('home')
    else:
        question_form = QuestionAddForm()
        formset = choice_form_set()

    context = {
        'question_form': question_form,
        'choices_forms': formset,
    }
    return render(request, 'polls/create_question.html', context)


def show_question(request, question_slug):
    question = get_object_or_404(Question, slug=question_slug)

