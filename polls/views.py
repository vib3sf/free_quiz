from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *


def index(request):
    return render(request, "polls/home.html")


@login_required
def create_poll(request):
    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        if poll_form.is_valid():
            poll = poll_form.save(commit=False)
            poll.creator_id = request.user.id
            poll.save()
            return redirect('show_poll', poll.id)
    else:
        poll_form = PollForm()

    context = {
        'poll_form': poll_form,
    }
    return render(request, 'polls/create_or_edit_poll.html', context)


def show_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    questions = poll.question_set.all()
    choices = {}
    for question in questions:
        choices[question] = question.choice_set.all()
    context = {
        'poll': poll,
    }
    return render(request, 'polls/show_poll.html', context)


@login_required
def create_question(request, poll_id):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.poll_id = poll_id
            question.save()
            return redirect('show_poll', poll_id)
    else:
        question_form = QuestionForm()

    context = {
        'form': question_form,
    }
    return render(request, 'polls/create_or_edit_question.html', context)


def edit_question(request, question_id):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        question = get_object_or_404(Question, id=question_id)
        if form.is_valid():
            question.question_text = form.cleaned_data['question_text']
            question.save()
            return redirect('show_poll', get_object_or_404(Question, id=question_id).poll_id)
    form = QuestionForm()
    context = {
        "form": form
    }
    return render(request, "polls/create_or_edit_question.html", context)


def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    question.delete()
    return redirect('show_poll', question.poll_id)


def add_choice(request, question_id):
    if request.method == "POST":
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.question_id = question_id
            choice.save()
            return redirect('show_poll', get_object_or_404(Question, id=question_id).poll_id)

    form = ChoiceForm()
    context = {
        "form": form
    }
    return render(request, "polls/create_or_edit_choice.html", context)


def edit_choice(request, choice_id):
    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        choice = get_object_or_404(Choice, id=choice_id)
        if form.is_valid():
            choice.choice_text = form.cleaned_data['choice_text']
            choice.save()
            return redirect('show_poll', choice.question.poll_id)
    form = ChoiceForm()
    context = {
        "form": form
    }
    return render(request, "polls/create_or_edit_choice.html", context)


def delete_choice(request, choice_id):
    choice = get_object_or_404(Choice, id=choice_id)
    choice.delete()
    return redirect('show_poll', choice.question.poll_id)


@login_required
def vote(request, choice_id):
    choice = get_object_or_404(Choice, id=choice_id)
    for v in Vote.objects.all():
        if v.voter == request.user and v.choice.question == choice.question:
            v.choice = choice
            v.save()
            break
    else:
        Vote(voter=request.user, choice=choice).save()
    return redirect('show_poll', choice.question.poll_id)
