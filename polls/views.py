from django.shortcuts import render


def index(request):
    return render(request, "polls/index.html")


def login(request):
    return render(request, "polls/login.html")


def create_quest(request):
    return render(request, "polls/create_quest.html")
