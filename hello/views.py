from django.shortcuts import *
from django.http import HttpResponse, Http404
from django.contrib.auth import *
from django.contrib.auth.models import User
from .forms import *
from .models import *
from django.template import RequestContext
from django.core.mail import send_mail
from django.views.generic.edit import UpdateView
from hello.models import Game
from hashlib import md5


def index(request):
    return render(request, 'index.html')


def games(request):
    return render(request, 'games.html', {"allgames": Game.objects.all()})


def game(request, name):
    return render(request, 'game.html', {"game": Game.objects.get(game_name=name.replace("_", " "))})


def profile_developer(request):
    return render(request, 'profile_developer.html')


def profile_player(request):
    return render(request, 'profile_player.html')


def delete_game(request):
    return render(request, 'delete_game.html', {"allgames": Game.objects.filter(game_developer=request.user)})


def registration(request):
    # registered = True

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
            # user_db.active = True
            # user_db.save()
            # login(request, user_db) # 3ICE: Don't bloody try to log in when it's not an activated account...
            dev = request.POST.get("developer", "not_developer") == "developer_box"
            user_db.developer = dev
            user_db.save()
            player = Player.objects.create(user=user_db, developer=dev, activated=False)
            hashed_password = user_db.password
            send_confirmation_mail(name, hashed_password, email)
            # if dev in ["developer_box"]: #3ICE: This is not how you check the existence of a checkbox.
            #    return redirect('registration')
            # else:
            #    return redirect('profile_player')
            return redirect('login')
        else:
            return render(request, 'signup.html', {'form': form})  # displays all errors in red automatically

    else:
        form = SignUpForm()  # 3ICE: Possibly stop using this, since we need to send the email
    return render(request, 'signup.html', {'form': form})


def addgame(request):
    if request.user.is_authenticated():
        if request.method == 'POST' or True:  # TODO Don't use "or True", it skips the if check entirely
            form = AddGameForm(data=request.POST)
            if form.is_valid():
                game = form.save(commit=False)
                game.game_developer = request.user
                game_edited = Game.objects.filter(game_name=game_name)
                game_edited_price=Game.objects.filter(game_price=game_price)
                game.game_name=game_edited_price
            else:
                print(form.errors)
            return render(request, "add_game.html", {"form": form})
        else:
            return redirect("login")
    else:
        return redirect("login")


def game_confirmation_delete(request, game_name):
    if request.user.is_authenticated():
        try:
            game = Game.objects.get(game_name=game_name)
        except Game.DoesNotExist:
            return redirect("delete_game")
        if not game:
            return redirect("delete_game")
        player = Player.objects.get(user=request.user)
        if request.user == game.game_developer:
            game.delete()
        else:
            raise Http404(
                "<h2>You are not authorized to delete this game!</h2><p>You are logged in as " + request.user.username + " but the game can only be delted by " + game.game_developer.username)
        return render(request, "game_confirmation_delete.html", {"game": game})
    else:
        return redirect("login")


def edit_game(request, game_name):
    try:
        game = Game.objects.get(game_name=game_name)
    except Game.DoesNotExist:
        return redirect("update")
    if not game:
        return redirect("update")
    if request.user.is_authenticated():
        if request.method == 'POST' or True:  # TODO Don't use "or True", it skips the if check entirely
            game_edited = Game.objects.get(game_name)
            form = EditGameForm(data=game_edited)
            if form.is_valid():
                new_game_data = form.save(commit=False)
                if(new_game_data.game_developer == request.user):
                    game_edited.game_name=new_game_data.game_name
                    game_edited.game_price=new_game_data.game_price
                    game_edited.game_url=new_game_data.game_url
                    game_edited.save()
                else:
                    raise Http404(
                        "<h2>You are not authorized to delete this game!</h2><p>You are logged in as " + request.user.username + " but the game can only be delted by " + game.game_developer.username)
            else:
                print(form.errors)
            return render(request, "update.html", {"form": form})
        else:
            return redirect("login")
    else:
        return redirect("login")

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

    # <a href="https://daak-store.herokuapp.com/user_verification/""" + secure_link + """
    # ">https://daak-store.herokuapp.com/user_verification/""" + secure_link + """</a>
    send_mail('Please confirm your registration at DAAK store, ' + name,
              msg, 'daaktest@gmail.com', [email])


# Verifying the user account
def user_verification(request, secure_link):
    name, pwd = secure_link.split('$$$$')
    user = User.objects.filter(username=name, password=pwd)
    # Player knows if he's a developer or not:
    player = Player.objects.get(user=user)
    if player:
        # user.update(active = True)
        player.activated = True
        player.save()
        msg = "We have validated your email id!"
    else:
        msg = "Verification error!"
    if player.developer:  # request.user.developer didn't work, so here's a workaround
        return render(request, 'profile_developer.html', {'msg': msg})
    else:
      return render(request, 'profile_player.html', {'msg': msg})

#payment logic
def pay_begin(request, game_name):
    if request.user.is_authenticated():
        game = Games.objects.get(game_name=game_name)
        pid = request.user.username
        pid+= game_name
        sid = "DanielArjunAparajitaKrishna"
        price = game.game_price
        secret_key = "5fe36a21b3cee01cb248a127892391de"
        check_string ="pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secret_key)
        m = md5(check_string.encode("ascii"))
        checksum = m.hexdigest()
        return render(request,'pay_begin.html',{'game_name':game_name,'pid':pid,'price':price,'checksum':checksum} )
    else:
        return redirect("login")
