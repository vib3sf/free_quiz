from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from .forms import *
from .models import *


class Home(TemplateView):
    template_name = 'polls/home.html'


class CreatePoll(CreateView):
    form_class = PollForm
    template_name = 'polls/create_or_edit_poll.html'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class EditPoll(UpdateView):
    form_class = PollForm
    template_name = 'polls/create_or_edit_poll.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Poll, id=self.kwargs['poll_id'])


class DeletePoll(DeleteView):
    template_name = 'polls/confirm_delete.html'

    def get_success_url(self):
        return reverse('home')

    def get_object(self, queryset=None):
        return get_object_or_404(Poll, id=self.kwargs['poll_id'])


class ShowPoll(DetailView):
    model = Poll
    template_name = 'polls/show_poll.html'
    pk_url_kwarg = 'poll_id'


class CreateQuestion(CreateView):
    form_class = QuestionForm
    template_name = 'polls/create_or_edit_question.html'

    def get_success_url(self):
        return reverse('show_poll', kwargs={'poll_id': self.kwargs['poll_id']})

    def form_valid(self, form):
        form.instance.poll_id = self.kwargs['poll_id']
        return super().form_valid(form)


class EditQuestion(UpdateView):
    form_class = QuestionForm
    template_name = 'polls/create_or_edit_question.html'

    def get_success_url(self):
        return reverse('show_poll', kwargs={'poll_id': self.get_object().poll_id})

    def get_object(self, queryset=None):
        return get_object_or_404(Question, id=self.kwargs['question_id'])


class DeleteQuestion(DeleteView):
    template_name = 'polls/confirm_delete.html'

    def get_success_url(self):
        return reverse('show_poll', kwargs={'poll_id': self.get_object().poll_id})

    def get_object(self, queryset=None):
        return get_object_or_404(Question, id=self.kwargs['question_id'])


class CreateChoice(CreateView):
    form_class = ChoiceForm
    template_name = 'polls/create_or_edit_choice.html'

    def get_success_url(self):
        return reverse('show_poll', kwargs={'poll_id': get_object_or_404(
            Question, id=self.kwargs['question_id']).poll_id})

    def form_valid(self, form):
        form.instance.question_id = self.kwargs['question_id']
        return super().form_valid(form)


class EditChoice(UpdateView):
    form_class = ChoiceForm
    template_name = 'polls/create_or_edit_question.html'

    def get_success_url(self):
        return reverse('show_poll', kwargs={'poll_id': self.get_object().question.poll_id})

    def get_object(self, queryset=None):
        return get_object_or_404(Choice, id=self.kwargs['choice_id'])


class DeleteChoice(DeleteView):
    template_name = 'polls/confirm_delete.html'

    def get_success_url(self):
        return reverse('show_poll', kwargs={'poll_id': self.get_object().question.poll_id})

    def get_object(self, queryset=None):
        return get_object_or_404(Choice, id=self.kwargs['choice_id'])


@login_required
def vote(request, choice_id):
    choice = get_object_or_404(Choice, id=choice_id)
    Vote.objects.filter(choice__question=choice.question, voter=request.user).update_or_create(
        voter=request.user, defaults={'choice': choice})
    return redirect('show_poll', choice.question.poll_id)
