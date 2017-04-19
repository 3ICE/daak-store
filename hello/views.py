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
    return render(request, 'game.html')

def profile_developer(request):
    return render(request, 'profile_developer.html')
def player(request):
    return render(request, 'player.html')
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
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            developer = request.POST.get("developer", None)
            if developer in ["developer_box"]:
                mail(user)
                return redirect('registration')
            else:
                mail(user)
                return redirect('player')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def addgame(request):
    if request.user.is_authenticated():
        if request.method == 'POST' or True:
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


# email validation
def mail(user):

    user_details = "%s:::%s"%(user.username, user.password)
    subject = 'Registration confirmation mail'
    message = 'Dear ' + user.username + ''',
Thank you for registering in daak-store of awesome stuffs.
We have validated your email id.
Kindly login again to continue by clicking on this link: https://daak-store.herokuapp.com/login/''' + user_details + '''

Best regards,
The Daak team'''
    recipient_list = []
    recipient_list.append(user.email)
    send_mail(subject, message, 'daaktest@gmail.com', recipient_list, fail_silently=False)




#Varifying the user account
#def user_verification(request, user_details):
#
#    username, password = user_details.split(':::')
#    user = User.objects.filter(username=username, password=password)
#    if user is not None:
#        user.update(is_active = True)
#        message = "Your account is now verified!"
#    else:
#        message = "Verification error!"
#
#   return render_to_response('profile_developer',context_instance=RequestContext(request, {'message': message}))


