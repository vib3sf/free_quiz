from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import PollForm, QuestionForm, ChoiceForm
from .models import Poll, Question, Choice, Vote


class Home(TemplateView):
    template_name = 'polls/home.html'


@method_decorator(login_required, name="dispatch")
class CreatePoll(CreateView):
    form_class = PollForm
    template_name = 'polls/create_or_edit_poll.html'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class EditPoll(UpdateView):
    form_class = PollForm
    template_name = 'polls/create_or_edit_poll.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Poll, id=self.kwargs['poll_id'])


@method_decorator(login_required, name="dispatch")
class DeletePoll(DeleteView):
    template_name = 'polls/confirm_delete.html'

    def get_success_url(self):
        return reverse('home')

    def get_object(self, queryset=None):
        return get_object_or_404(Poll, id=self.kwargs['poll_id'])


@method_decorator(login_required, name="dispatch")
class ShowPoll(DetailView):
    model = Poll
    template_name = 'polls/show_poll.html'
    pk_url_kwarg = 'poll_id'


@method_decorator(login_required, name="dispatch")
class CreateQuestion(CreateView):
    form_class = QuestionForm
    template_name = 'polls/create_or_edit_question.html'

    def get_success_url(self):
        return reverse('show_poll', kwargs={'poll_id': self.kwargs['poll_id']})

    def form_valid(self, form):
        form.instance.poll_id = self.kwargs['poll_id']
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class EditQuestion(UpdateView):
    form_class = QuestionForm
    template_name = 'polls/create_or_edit_question.html'

    def get_success_url(self):
        return reverse('show_poll', kwargs={'poll_id': self.get_object().poll_id})

    def get_object(self, queryset=None):
        return get_object_or_404(Question, id=self.kwargs['question_id'])


@method_decorator(login_required, name="dispatch")
class DeleteQuestion(DeleteView):
    template_name = 'polls/confirm_delete.html'

    def get_success_url(self):
        return reverse('show_poll', kwargs={'poll_id': self.get_object().poll_id})

    def get_object(self, queryset=None):
        return get_object_or_404(Question, id=self.kwargs['question_id'])


@method_decorator(login_required, name="dispatch")
class CreateChoice(CreateView):
    form_class = ChoiceForm
    template_name = 'polls/create_or_edit_choice.html'

    def get_success_url(self):
        return reverse('show_poll', kwargs={'poll_id': get_object_or_404(
            Question, id=self.kwargs['question_id']).poll_id})

    def form_valid(self, form):
        form.instance.question_id = self.kwargs['question_id']
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class EditChoice(UpdateView):
    form_class = ChoiceForm
    template_name = 'polls/create_or_edit_question.html'

    def get_success_url(self):
        return reverse('show_poll', kwargs={'poll_id': self.get_object().question.poll_id})

    def get_object(self, queryset=None):
        return get_object_or_404(Choice, id=self.kwargs['choice_id'])


@method_decorator(login_required, name="dispatch")
class DeleteChoice(DeleteView):
    template_name = 'polls/confirm_delete.html'

    def get_success_url(self):
        return reverse('show_poll', kwargs={'poll_id': self.get_object().question.poll_id})

    def get_object(self, queryset=None):
        return get_object_or_404(Choice, id=self.kwargs['choice_id'])


@method_decorator(login_required, name='dispatch')
class Pick(View):
    def get(self, request, *args, **kwargs):
        choice = get_object_or_404(Choice, id=kwargs['choice_id'])
        Vote.objects.filter(choice__question=choice.question, voter=request.user).update_or_create(
            voter=request.user, defaults={'choice': choice})
        return redirect(choice.question.poll)
