from polls.models import Poll
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
import django.contrib.auth as log
from django.shortcuts import render, redirect, reverse
from .forms import UserRegisterForm


class Register(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def get_success_url(self):
        return reverse('home')


class Profile(ListView):
    template_name = "users/profile.html"
    model = Poll

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'user_polls': self.request.user.poll_set.all(),
            'completed_polls': Poll.objects.filter(question__choice__vote__voter=self.request.user)
        })
        return context


@login_required
def logout(request):
    log.logout(request)
    return redirect('home')
