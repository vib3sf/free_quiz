from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, DeleteView

from free_quiz.mixins.mixins import TitleMixin
from .forms import PollForm
from .models import Poll, Question, Choice, Vote


class Home(TitleMixin, TemplateView):
    template_name = 'polls/home.html'
    title = 'Home'


@method_decorator(login_required, name='dispatch')
class ShowPoll(TitleMixin, DetailView):
    model = Poll
    template_name = 'polls/show_poll.html'
    pk_url_kwarg = 'poll_id'

    def get_title(self):
        return self.get_object()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        poll = self.get_object()

        context.update({
            'poll_completed': poll.user_completed_poll(self.request.user),
            'can_vote': poll.user_can_vote(self.request.user),
            'selected_choices': Choice.objects.filter(vote__voter=self.request.user, question__poll=poll)
        })
        return context


@method_decorator(login_required, name="dispatch")
class CreatePoll(TitleMixin, FormView):
    form_class = PollForm
    template_name = 'polls/create.html'
    title = 'Create poll'


@login_required
def create(request):
    poll = PollForm(request.POST).save(commit=False)
    poll.creator = request.user
    poll.save()

    questions = [(name, value) for name, value in request.POST.items() if name.startswith('question_')]

    if not questions:
        messages.error(request, 'Poll must have at least on question')
        poll.delete()
        return redirect('create_poll')

    for question_name, question_value in questions:
        question = Question(question_text=question_value, poll_id=poll.id)

        choices = [(choice_name, choice_value) for choice_name, choice_value in request.POST.items()
                   if choice_name.startswith(f'choice_{question_name}')]

        if not choices:
            messages.error(request, 'Questions must have at least one choice')
            poll.delete()
            return redirect('create_poll')

        question.save()
        for choice_name, choice_value in choices:
            Choice(choice_text=choice_value, question_id=question.id).save()

    return redirect('show_poll', poll.id)


@method_decorator(login_required, name='dispatch')
class DeletePoll(TitleMixin, UserPassesTestMixin, DeleteView):
    model = Poll
    template_name = 'polls/confirm_delete.html'
    pk_url_kwarg = 'poll_id'
    title = 'Confirm delete'
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user == self.get_object().creator


@method_decorator(login_required, name='dispatch')
class Pick(TitleMixin, UserPassesTestMixin, DetailView):
    model = Poll
    template_name = 'polls/vote.html'
    pk_url_kwarg = 'poll_id'

    def get_title(self):
        return self.get_object()

    def test_func(self):
        return self.get_object().user_can_vote(self.request.user)


@login_required
def vote(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if not poll.user_can_vote(request.user):
        raise PermissionDenied

    for question in poll.question_set.all():
        selected_choice = question.choice_set.get(id=request.POST[f"{question.id}"])
        Vote.objects.filter(choice__question=selected_choice.question, voter=request.user) \
            .update_or_create(voter=request.user, defaults={'choice': selected_choice})
    return redirect(poll)
