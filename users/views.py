from django.urls import reverse_lazy
from polls.models import Poll
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from .forms import UserRegisterForm


class Register(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')


@method_decorator(login_required, name="dispatch")
class Profile(TemplateView):
    template_name = "users/profile.html"
    model = Poll

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_polls = self.request.user.poll_set.all()
        completed_polls = Poll.objects.filter(
            question__choice__vote__voter=self.request.user,
        ).distinct().exclude(id__in=user_polls)
        context.update({
            'user_polls': user_polls,
            'completed_polls': completed_polls
        })
        return context
