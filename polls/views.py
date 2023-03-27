from django.shortcuts import render


def index(request):
    return render(request, "polls/home.html")


def create_quest(request):
    return render(request, "polls/create_quest.html")
