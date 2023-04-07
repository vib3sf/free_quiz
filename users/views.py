from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
import django.contrib.auth as log
from django.shortcuts import render, redirect, reverse
from .forms import UserRegisterForm


class Register(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def get_success_url(self):
        return reverse('home')


@login_required
def profile(request):
    context = {
        'polls': request.user.poll_set.all(),
    }
    return render(request, 'users/profile.html', context)


@login_required
def logout(request):
    log.logout(request)
    return redirect('home')
