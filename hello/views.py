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
            email = form.cleaned_data.get('email')
            user = authenticate(username=name, password=raw_password)
            # 3ICE: Temporarily auth them (worked like this before)
            #user_db.active = True
            #user_db.save()
            #login(request, user_db) # 3ICE: Don't bloody try to log in when it's not an activated account...
            dev = request.POST.get("developer", None)
            user_db.developer=dev
            user_db.save()
            player=Player.objects.create(user=user_db, developer=dev)
            player=Player.objects.create(user=user, developer=dev)
            hashed_password = user_db.password
            send_confirmation_mail(name, hashed_password, email)
            #if dev in ["developer_box"]:
            #    return redirect('registration')
            #else:
            #    return redirect('profile_player')
            return redirect('login')
        else: return render(request, 'signup.html', {'form': form}) # displays all errors in red automatically
          
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
def send_confirmation_mail(name, pw, email):
    secure_link = name + "$$$$" + pw
    msg = """
          Dear %(name)s,
          Welcome to DAAK store!
          Thank you for registering in our store of awesome stuffs.
          
          We will validate your id promptly.
          Please click this link to verify you email address and complete registration:
          https://daak-store.herokuapp.com/user_verification/%(link)s
          And then kindly login again to continue.
          
          Best regards,
          The DAAK team of awesome stuffs!
          http://daak-store.herokuapp.com/
          """ % {'name': name, 'link': secure_link}

    #<a href="https://daak-store.herokuapp.com/user_verification/""" + secure_link + """
    #">https://daak-store.herokuapp.com/user_verification/""" + secure_link + """</a>
    send_mail('Please confirm your registration at DAAK store, ' + name,
              msg, 'daaktest@gmail.com', [email])

#Verifying the user account
def user_verification(request, secure_link):
    name, pwd = secure_link.split('$$$$')
    user = User.objects.filter(username=name, password=pwd)
    # Player knows if he's a developer or not:
    player = Player.objects.get(user=user)
    if player:
        user.update(active = True)
        player.update(activated = True)
        user.save()
        msg = "We have validated your email id!"
    else:
        msg = "Verification error!"
    if player.developer: #request.user.developer didn't work, so here's a workaround
      return render(request, 'profile_developer.html', {'msg': msg})
    else:
      return render(request, 'profile_player.html', {'msg': msg})

