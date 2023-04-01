from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify
from .forms import *


def index(request):
    return render(request, "polls/home.html")


@login_required
def create_question(request):
    if request.method == 'POST':
        question_form = QuestionAddForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.creator_id = request.user.id
            question.slug = slugify(question.question_text)
            question.save()
            return redirect('show_question', question.id)
    else:
        question_form = QuestionAddForm()
        formset = ChoiceFormSet()

    context = {
        'question_form': question_form,
    }
    return render(request, 'polls/create_question.html', context)


def add_choice(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == "POST":
        form = ChoiceAddForm(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.question_id = question.id
            choice.save()
            print("I'm here")
            return redirect('show_question', question.id)

    form = ChoiceAddForm()
    context = {
        "form": form
    }
    return render(request, "polls/create_choice.html", context)


def delete_choice(request, choice_id):
    choice = get_object_or_404(Choice, id=choice_id)
    question = choice.question
    choice.delete()
    return redirect('show_question', question.id)


def show_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    choices = question.choice_set.all()
    context = {
        'question': question,
        'choices': choices,
    }
    return render(request, 'polls/show_question.html', context)


