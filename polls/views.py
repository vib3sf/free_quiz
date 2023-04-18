from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import PollForm, QuestionForm, ChoiceForm
from .models import Poll, Question, Choice, Vote
from django.db.models import Count


class Home(TemplateView):
    template_name = 'polls/home.html'


@method_decorator(login_required, name="dispatch")
class ShowPoll(DetailView):
    model = Poll
    template_name = 'polls/show_poll.html'
    pk_url_kwarg = 'poll_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        poll = self.get_object()
        context.update({
            'poll_completed': poll.user_completed_poll(self.request.user),
            'can_vote': poll.user_can_vote(self.request.user)
        })
        return context


@method_decorator(login_required, name='dispatch')
class CreateOrEditVote(UserPassesTestMixin, DetailView):
    model = Poll
    template_name = 'polls/vote.html'
    pk_url_kwarg = 'poll_id'

    def test_func(self):
        return self.get_object().user_can_vote(self.request.user)


@method_decorator(login_required, name="dispatch")
class Edit(UserPassesTestMixin, DetailView):
    model = Poll
    template_name = 'polls/edit.html'
    pk_url_kwarg = 'poll_id'

    def test_func(self):
        return self.get_object().creator == self.request.user


@method_decorator(login_required, name="dispatch")
class CreatePoll(CreateView):
    form_class = PollForm
    template_name = 'polls/create_or_edit.html'

    def get_success_url(self):
        return reverse('edit', kwargs={'poll_id': self.object.id})

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class EditPoll(UserPassesTestMixin, UpdateView):
    form_class = PollForm
    model = Poll
    template_name = 'polls/create_or_edit.html'
    pk_url_kwarg = 'poll_id'

    def test_func(self):
        return self.get_object().creator == self.request.user


@method_decorator(login_required, name="dispatch")
class DeletePoll(UserPassesTestMixin, DeleteView):
    template_name = 'polls/confirm_delete.html'
    model = Poll
    pk_url_kwarg = 'poll_id'
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.get_object().creator == self.request.user


@method_decorator(login_required, name="dispatch")
class CreateQuestion(UserPassesTestMixin, CreateView):
    form_class = QuestionForm
    model = Poll
    template_name = 'polls/create_or_edit.html'
    pk_url_kwarg = 'poll_id'

    def test_func(self):
        return self.get_object().creator == self.request.user

    def get_success_url(self):
        return reverse('edit', kwargs={'poll_id': self.kwargs['poll_id']})

    def form_valid(self, form):
        form.instance.poll_id = self.kwargs['poll_id']
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class EditQuestion(UserPassesTestMixin, UpdateView):
    form_class = QuestionForm
    model = Question
    template_name = 'polls/create_or_edit.html'
    pk_url_kwarg = 'question_id'

    def test_func(self):
        return self.get_object().poll.creator == self.request.user

    def get_success_url(self):
        return reverse('edit', kwargs={'poll_id': self.get_object().poll_id})


@method_decorator(login_required, name="dispatch")
class DeleteQuestion(UserPassesTestMixin, DeleteView):
    template_name = 'polls/confirm_delete.html'
    model = Question
    pk_url_kwarg = 'question_id'

    def test_func(self):
        return self.get_object().poll.creator == self.request.user

    def get_success_url(self):
        return reverse('edit', kwargs={'poll_id': self.get_object().poll_id})


@method_decorator(login_required, name="dispatch")
class CreateChoice(UserPassesTestMixin, CreateView):
    form_class = ChoiceForm
    model = Question
    template_name = 'polls/create_or_edit.html'
    pk_url_kwarg = 'question_id'

    def test_func(self):
        return self.get_object().poll.creator == self.request.user

    def get_success_url(self):
        return reverse('edit', kwargs={'poll_id': self.get_object().poll_id})

    def form_valid(self, form):
        form.instance.question_id = self.kwargs['question_id']
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class EditChoice(UserPassesTestMixin, UpdateView):
    form_class = ChoiceForm
    model = Choice
    template_name = 'polls/create_or_edit.html'
    pk_url_kwarg = 'choice_id'

    def test_func(self):
        return self.get_object().question.poll.creator == self.request.user

    def get_success_url(self):
        return reverse('edit', kwargs={'poll_id': self.get_object().question.poll_id})


@method_decorator(login_required, name="dispatch")
class DeleteChoice(UserPassesTestMixin, DeleteView):
    template_name = 'polls/confirm_delete.html'
    model = Choice
    pk_url_kwarg = 'choice_id'

    def test_func(self):
        return self.get_object().question.poll.creator == self.request.user

    def get_success_url(self):
        return reverse('edit', kwargs={'poll_id': self.get_object().question.poll_id})


@method_decorator(login_required, name="dispatch")
class Pick(UserPassesTestMixin, DetailView):
    model = Choice
    pk_url_kwarg = 'choice_id'

    def test_func(self):
        return self.get_object().question.poll.user_can_vote(self.request.user)

    def get(self, request, *args, **kwargs):
        Vote.objects.filter(choice__question=self.get_object().question, voter=request.user)\
            .update_or_create(voter=request.user, defaults={'choice': self.get_object()})
        return redirect('vote', self.get_object().question.poll.id)


@method_decorator(login_required, name="dispatch")
class FinishPoll(UserPassesTestMixin, DetailView):
    model = Poll
    pk_url_kwarg = 'poll_id'

    def test_func(self):
        return self.get_object().user_can_vote(self.request.user)

    def get(self, request, *args, **kwargs):
        poll = self.get_object()
        votes = Vote.objects.filter(choice__question__poll=poll, voter=request.user)
        if votes.count() == Question.objects.annotate(choice_count=Count('choice'))\
                .filter(poll=poll, choice_count__gte=1).count():
            votes.update(poll_finished=True)
            return redirect('show_poll', poll.id)
        return redirect('vote', poll.id)
