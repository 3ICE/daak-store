from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate

from .models import Greeting
from .forms import SignUpForm

def index(request):
    return render(request, 'index.html')


def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, 'db.html', {'greetings': greetings})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            developer =request.POST.get("developer", None)
            if developer in ["developer_box"]:
                return redirect('profile_developer')
            else:
                login(request, user)
                return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})