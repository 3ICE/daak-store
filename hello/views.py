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

# FOR RESTFUL ScoreSerializer
from hello.serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json


# landing page
def index(request):
    return render(request, 'index.html', {"allgames": Game.objects.all()})



# list of games
def games(request):
    if request.user.is_authenticated():
        return render(request, 'games.html', {"allgames": Game.objects.all()})


# def scores(request):
#     if request.user.is_authenticated():
#         return render(request, 'loadhighscores.html', {"allscores": Score.objects.all()})


# link to a particular game
def game(request, name):
    if request.user.is_authenticated():
        game = Game.objects.get(game_name=name)
        # 3ICE: Player doesn't have a "receipt" in the Score database table, so make them buy first
        if Score.objects.filter(game=game, player=request.user).exists():
            return render(request, 'game.html', {"game": Game.objects.get(game_name=name.replace("_", " "))})
        else:
            return redirect('../pay_begin/' + name)


# link to developer's view
def profile_developer(request):

    if request.user.is_authenticated():
        try:
            player = Player.objects.get(user=request.user)
            if(player):
                if player.developer:
                    return render(request, 'profile_developer.html')
        except:
            return redirect('profile_player')
    return redirect('profile_player')


# link to player view
def profile_player(request):
    if request.user.is_authenticated():
        return render(request, 'profile_player.html')


# linking page to options with delete, add and edit games
def manage_game(request):
    if request.user.is_authenticated():
        return render(request, 'manage_game.html', {"allgames": Game.objects.filter(game_developer=request.user)})


# linking to registration
def registration(request):
    # registered = True

    return render(request, 'registration.html')


# takes to the sign up page
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
            dev = request.POST.get("developer", "not_developer") == "developer_box"  # check if developer
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


# checks if user is developer and lets him add his game
def addgame(request):
    if request.user.is_authenticated():
        if request.method == 'POST' or True:  # TODO Don't use "or True", it skips the if check entirely
            form = AddGameForm(data=request.POST)
            if form.is_valid():
                game = form.save(commit=False)
                game.game_developer = request.user  # gets user
                game.save()  # saves
            else:
                print(form.errors)
            return render(request, "add_game.html", {"form": form})
        else:
            return redirect("login")
    else:
        return redirect("login")


# checks if it is developers game and lets him delete his game
def game_confirmation_delete(request, game_name):
    if request.user.is_authenticated():
        try:
            game = Game.objects.get(game_name=game_name)  # get the game based on the name
        except Game.DoesNotExist:
            return redirect("manage_game")
        if not game:
            return redirect("manage_game")
        player = Player.objects.get(user=request.user)  # get players info to check if developer
        if request.user == game.game_developer:
            game.delete()  # lets them delete if developer
        else:
            raise Http404(
                "<h2>You are not authorized to delete this game!</h2><p>You are logged in as " + request.user.username + " but the game can only be deleted by " + game.game_developer.username)
        return render(request, "game_confirmation_delete.html", {"game": game})
    else:
        return redirect("login")


# checks if the user is a developer and lets him change name game price and url to the game
def edit_game(request, game_name):
    try:
        game_edited = Game.objects.get(game_name=game_name)  # gets the game based on its name
    except Game.DoesNotExist:
        return redirect("manage_game")
    if not game_edited:
        return redirect("manage_game")
    if request.user.is_authenticated():
        form = EditGameForm(
            {'game_name': game_name, 'game_price': game_edited.game_price,
             'game_url': game_edited.game_url})  # get original information of the game
        if request.method == 'POST':
            # lets user edit game if he is developer and it is added by him
            if form.is_valid():
                if (game_edited.game_developer == request.user):
                    game_edited.game_name = request.POST['game_name']
                    game_edited.game_price = request.POST['game_price']
                    game_edited.game_url = request.POST['game_url']
                    game_edited.save()
                    return redirect("manage_game")
                else:  # 3ICE: Logged in as wrong user?
                    raise Http404(
                        "<h2>You are not authorized to edit this game!</h2><p>You are logged in as " + request.user.username + " but the game can only be edited by " + game_edited.game_developer.username)
            else:  # 3ICE: Form not valid, somehow... document.forms[0].submit() maybe?
                print(form.errors)
                return render(request, "update.html", {'form': form})
        else:  # 3ICE: request is nto POST, they don't have  form yet, let's give it to them now:
            return render(request, "update.html", {'form': form})
    else:  # 3ICE: Authentication fail #1 TODO: Check if they activated their account with player (No, not User).
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


# payment logic
def md5hex(tohash):
    """
  Calculates an MD5 checksum for the given string.
  """
    try:
        import hashlib  # Python >=2.5
        m = hashlib.md5()
    except:  # Python <2.5
        import md5
        m = md5.new()
    m.update(tohash)
    return m.hexdigest()


# takes to confirmation payment page
# regular expression fix
def make_pid(username, game_name):
    pid = username
    pid += '____'
    pid += game_name
    return pid


def pay_begin(request, game_name):
    if request.user.is_authenticated():
        game = Game.objects.get(game_name=game_name)
        pid = make_pid(request.user.username, game_name)  # re to concat username and game user wants to buy
        sid = "DanielArjunAparajitaKrishna"
        price = game.game_price
        secret_key = "5fe36a21b3cee01cb248a127892391de"

        # 3ICE: Unrelated failures:
        check_string = "pid=" + pid + "&sid=" + sid + "&amount=" + str(price) + "&token=" + secret_key
        checksum = md5(check_string.encode("ascii")).hexdigest()
        checkstr = "pid=%s&sid=%s&amount=%s&token=%s" % (pid, sid, price, secret_key)

        # 3ICE: Thanks to tophattop on slack for prompt assistance:
        check_top_hat = 'pid={}&sid={}&amount={}&token={}'.format(pid, sid, price, secret_key)

        # 3ICE: In the end it was setting the form input "disabled" that caused the error. Not the above.

        return render(request, 'pay_begin.html', {'game_name': game_name, 'pid': pid, 'price': price,
                                                  'checksum': md5hex(check_top_hat.encode("ascii"))})
    else:
        return redirect("login")


# payment succeeded
def pay_success(request):
    if request.user.is_authenticated():
        pid = request.GET['pid']
        checksum = request.GET['checksum']
        ref = request.GET['ref']
        result = request.GET['result']
        sid = "DanielArjunAparajitaKrishna"
        secret_key = "5fe36a21b3cee01cb248a127892391de"
        username, game_name = pid.split('____')
        game = Game.objects.get(game_name=game_name)
        check_top_hat = 'pid={}&ref={}&result={}&token={}'.format(pid, ref, result, secret_key)
        # check_string = "pid=" + pid + "&sid=" + sid + "&amount=" + str(price) + "&token=" + secret_key
        # m = md5(check_string.encode("ascii"))

        if md5hex(check_top_hat.encode("ascii")) == checksum:

            user = User.objects.get(username=username)
            if Score.objects.filter(game=game, player=user).exists():
                raise Http404(
                    "<h2> You don't have to pay us twice!,You already have the game in your inventory " + user.username)
            else:
                # 3ICE: This is the "receipt" for having purchased the game.
                Score.objects.create(game=game, player=user, score=0)

                # 3ICE: Record sales statistics
                game.game_sales += 1
                game.save()
            return render(request, 'pay_success.html', {'game': game})
        else:
            return render(request, 'pay_failed.html')
    else:
        return redirect("login")
        # create a logic which takes care of checking whether player has already bought the game
        # if the player has already purchased, throw error, navigate back to the game
        # else add player to the game or vice versa, navigate back to the games list


# payment cancelled
def pay_cancel(request):
    if request.user.is_authenticated():
        return render(request, 'pay_cancel.html')
    else:
        return redirect("login")


# payment error
def pay_failed(request):
    if request.user.is_authenticated():
        return render(request, 'pay_failed.html')
    else:
        return redirect("login")


# displaying high scores in the high scores page
@api_view(['GET'])
def highscores(request, game_name):
    if request.user.is_authenticated() and not request.user.is_anonymous():
        game = Game.objects.get(game_name=game_name)
        scores = Score.objects.filter(game=game)

        if request.method == 'GET':
            #serializer = ScoreSerializer(scores, many=True)
            dump = {"game": game.game_name}

            for score in scores:
                dump.append((score.user.username:score.score)):

            return Response(Json.dumps(dump))
    else:
        return redirect("login")


@api_view(['GET'])
def highscore(request, game_name, player_name):
    if request.user.is_authenticated() and not request.user.is_anonymous():
        user = User.objects.get(username=user_name)
        game = Game.objects.get(game_name=game_name)
        score = Score.objects.filter(game=game, player=user)
        if request.method == 'GET':
            serializer = ScoreSerializer(score)
            return Response(serializer.data)
    else:
        return redirect("login")


def save(request):
    if request.method == 'POST' and request.is_ajax():
        data = json.loads(request.POST.get('state', None))
        state = data['gameState']
        states = json.dumps(state)
        states = states.decode('string_escape')
        # load player and game associated with this request, and use them to query the Scores object
        game_name = request.POST.get('game_name', None)
        player_name = request.POST.get('player_name', None)
        game = Game.objects.get(game_name=game_name)
        user = User.objects.get(username=player_name)
        score = Score.objects.filter(game=game, player=user)
        # score.update(score=state["gameState"])
        score.update(state=states)
        return HttpResponse(states, content_type='application/json')
    else:
        raise Http404('Not a POST request, not an AJAX request, what are you doing?')


def load(request):
    if request.method == 'POST' and request.is_ajax():
        data = json.loads(request.POST.get('json', None))
        game_name = request.POST.get('game_name', None)
        player_name = request.POST.get('player_name', None)
        game = Game.objects.get(game_name=game_name)
        user = User.objects.get(username=player_name)
        score = Score.objects.get(game=game, player=user)

        data["messageType"] = "LOAD"
        data["gameState"] = score.state
        if score.state:
            data["messageType"] = "LOAD"
            data["gameState"] = score.state

        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404('Not a POST request, not an AJAX request, what are you doing?')


# def loadhighscores(request, id):
#     if request.user.is_authenticated():
#         player = request.user
#         game = Score.objects.get(game=game)
#         return render_to_response('highscores.html', {'player': player, 'game': game, 'score': score})
#     else:
#         return redirect('login.html')
