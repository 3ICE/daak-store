from django.shortcuts import *
from django.http import HttpResponse
from django.contrib.auth import *
from django.contrib.auth.models import User
from .forms import *
from .models import *
from django.template import RequestContext
from django.core.mail import send_mail


def index(request):
    return render(request, 'index.html')

def games(request):
    return render(request, 'games.html',{"allgames":Game.objects.all()})

def game(request,name):
    return render(request, 'game.html',{"game":Game.objects.get(game_name=name.replace("_"," "))})

def profile_developer(request):
    return render(request, 'profile_developer.html')

def profile_player(request):
    return render(request, 'profile_player.html')

def delete_game(request):
    return render(request, 'delete_game.html', {"allgames": Game.objects.filter(game_developer=request.user)})

def registration(request):
    #registered = True
    
    return render(request, 'registration.html')

def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, 'db.html', {'greetings': greetings})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user_db = form.save(commit=False)
            name = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user_auth = authenticate(username=name, password=raw_password)
            player=Player.objects.filter(username=name)
            login(request, user_auth)
            developer = request.POST.get("developer", None)
            user_db.update(developer = True)
            user_db.save()
            if developer in ["developer_box"]:
                mail(user_auth)
                return redirect('registration')
            else:
                mail(user_auth)
                return redirect('profile_player')
    else:
        form = SignUpForm() # 3ICE: Possibly stop using this, since we need to send the email
    return render(request, 'signup.html', {'form': form})


def addgame(request):
    if request.user.is_authenticated():
        if request.method == 'POST' or True: # TODO Don't use "or True", it skips the if check entirely
            form = AddGameForm(data=request.POST)
            if form.is_valid():
                game = form.save(commit=False)
                game.game_developer = request.user
                game.save()
            else:
                print(form.errors)
            return render(request,"add_game.html", {"form": form})
        else:
            return redirect("login")
    else:
        return redirect("login")
def delete(request):
    if request.POST.get('delete'):
        obj.delete()


# email validation
def mail(user):
    secure_link = user.username + "$$$$" + user.password
    msg = 'Dear ' + user.username + """,
Welcome to DAAK store!
Thank you for registering in our store of awesome stuffs.

We will validate your email id promptly.
Please click this link to verify you email address and complete registration:
https://daak-store.herokuapp.com/user_verification/""" + secure_link + """

And then kindly login again to continue.

Best regards,
The Daak team
Thanks,
The DAAK team of awesome!
http://daak-store.herokuapp.com/
"""
    send_mail('Please confirm your registration at DAAK store, ' + user.username,
              msg, 'daaktest@gmail.com', [user.email])

#Verifying the user account
def user_verification(request, secure_link):
    name, pwd = secure_link.split('$$$$')
    user = Player.objects.filter(username=name, password=pwd)
    if user:
        user.update(active = True)
        user.save()
        msg = "We have validated your email id!"
    else:
        msg = "Verification error!"
    if request.user.developer:
      return render(request, 'profile_developer.html', {'msg': msg})
    else:
      return render(request, 'profile_player.html', {'msg': msg})

