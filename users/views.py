from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        r_form = UserRegisterForm(request.POST)
        if r_form.is_valid():
            r_form.save()
            messages.success(request, 'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        r_form = UserRegisterForm()
    return render(request, 'users/register.html', {'r_form': r_form})
