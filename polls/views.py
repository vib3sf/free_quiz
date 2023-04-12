from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import PollForm, QuestionForm, ChoiceForm
from .models import Poll, Question, Choice, Vote


class Home(TemplateView):
    template_name = 'polls/home.html'


@method_decorator(login_required, name="dispatch")
class ShowPoll(DetailView):
    model = Poll
    template_name = 'polls/show_poll.html'
    pk_url_kwarg = 'poll_id'


@method_decorator(login_required, name='dispatch')
class CreateOrEditVote(DetailView):
    model = Poll
    template_name = 'polls/vote.html'
    pk_url_kwarg = 'poll_id'


@method_decorator(login_required, name="dispatch")
class Edit(DeleteView):
    model = Poll
    template_name = 'polls/edit.html'
    pk_url_kwarg = 'poll_id'


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
class CreateQuestion(CreateView):
    form_class = QuestionForm
    template_name = 'polls/create_or_edit_question.html'

    def get_success_url(self):
        return reverse('edit', kwargs={'poll_id': self.kwargs['poll_id']})

    def form_valid(self, form):
        form.instance.poll_id = self.kwargs['poll_id']
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class EditQuestion(UpdateView):
    form_class = QuestionForm
    template_name = 'polls/create_or_edit_question.html'

    def get_success_url(self):
        return reverse('edit', kwargs={'poll_id': self.get_object().poll_id})

    def get_object(self, queryset=None):
        return get_object_or_404(Question, id=self.kwargs['question_id'])


@method_decorator(login_required, name="dispatch")
class DeleteQuestion(DeleteView):
    template_name = 'polls/confirm_delete.html'

    def get_success_url(self):
        return reverse('edit', kwargs={'poll_id': self.get_object().poll_id})

    def get_object(self, queryset=None):
        return get_object_or_404(Question, id=self.kwargs['question_id'])


@method_decorator(login_required, name="dispatch")
class CreateChoice(CreateView):
    form_class = ChoiceForm
    template_name = 'polls/create_or_edit_choice.html'

    def get_success_url(self):
        return reverse('edit', kwargs={'poll_id': get_object_or_404(Question, id=self.kwargs['question_id']).poll_id})

    def form_valid(self, form):
        form.instance.question_id = self.kwargs['question_id']
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class EditChoice(UpdateView):
    form_class = ChoiceForm
    template_name = 'polls/create_or_edit_question.html'

    def get_success_url(self):
        return reverse('edit', kwargs={'poll_id': self.get_object().question.poll_id})

    def get_object(self, queryset=None):
        return get_object_or_404(Choice, id=self.kwargs['choice_id'])


@method_decorator(login_required, name="dispatch")
class DeleteChoice(DeleteView):
    template_name = 'polls/confirm_delete.html'

    def get_success_url(self):
        return reverse('edit', kwargs={'poll_id': self.get_object().question.poll_id})

    def get_object(self, queryset=None):
        return get_object_or_404(Choice, id=self.kwargs['choice_id'])


@login_required
def pick(request, *args, **kwargs):
    choice = get_object_or_404(Choice, id=kwargs['choice_id'])
    Vote.objects.filter(choice__question=choice.question, voter=request.user)\
        .update_or_create(voter=request.user, defaults={'choice': choice})
    return redirect('vote', choice.question.poll.id)


@login_required
def finish_poll(request, *args, **kwargs):
    poll = get_object_or_404(Poll, id=kwargs['poll_id'])
    votes = Vote.objects.filter(choice__question__poll=poll, voter=request.user)
    if votes.count() == poll.question_set.count():
        votes.update(poll_finished=True)
        return redirect('show_poll', poll.id)
    return redirect('vote', poll.id)
