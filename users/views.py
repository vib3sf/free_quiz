from django.contrib.auth.decorators import login_required
import django.contrib.auth as log
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


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
