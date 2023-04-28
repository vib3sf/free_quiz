from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, reverse, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from free_quiz.mixins.mixins import TitleMixin
from .forms import PollForm
from .models import Poll, Question, Choice, Vote


class Home(TitleMixin, ListView):
    template_name = 'polls/home.html'
    model = Poll
    context_object_name = 'polls'
    title = 'Home'

    def get_queryset(self):
        return Poll.objects.order_by('-pub_date')[:5]


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


@method_decorator(login_required, name="dispatch")
class CreatePoll(FormView):
    form_class = PollForm
    template_name = 'polls/create.html'

    def get_success_url(self):
        return reverse('show_poll', kwargs={'poll_id': self.object.id})

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


def create(request):
    poll = PollForm(request.POST).save(commit=False)
    poll.creator = request.user
    poll.save()

    questions = [(name, value) for name, value in request.POST.items() if name.startswith('question_')]

    for question_name, question_value in questions:
        question = Question(question_text=question_value, poll_id=poll.id)
        question.save()

        choices = [(choice_name, choice_value) for choice_name, choice_value in request.POST.items()
                   if choice_name.startswith(f'choice_{question_name}')]

        for choice_name, choice_value in choices:
            Choice(choice_text=choice_value, question_id=question.id).save()
    return redirect('show_poll', poll.id)


@method_decorator(login_required, name='dispatch')
class Pick(UserPassesTestMixin, DetailView):
    model = Poll
    template_name = 'polls/vote.html'
    pk_url_kwarg = 'poll_id'

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
