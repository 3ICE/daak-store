from django.shortcuts import *
from django.http import HttpResponse
from django.contrib.auth import *
from django.contrib.auth.models import User
from .forms import add_Game_Form
from .models import *
from .forms import SignUpForm

def index(request):
    return render(request, 'index.html')
def profile_developer(request):
    return render(request,'profile_developer.html')

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
            login(request, user)
            developer =request.POST.get("developer", None)
            if developer in ["developer_box"]:

                return redirect('profile_developer')
            else:

                return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
def add_Game(request):
    if request.user.is_authenticated():
        if request.method=='POST':
            form = add_Game_Form(data=request.POST)
            if form.is_valid():
                game=form.save(commit=False)
                game.game_developer=request.user
                game.save()
            else:
                print(form.errors)
            return render_to_response("templates/add_game.html",{"form":form})
    else:
        raise Http404()