from django.shortcuts import render, redirect


def index(request):
    return render(request, "polls/home.html")


def create_question(request):
    if not request.user.is_authenticated:
        return redirect('register')
    return render(request, 'polls/create_quest.html')
