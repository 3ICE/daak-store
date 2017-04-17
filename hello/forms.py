from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from textwrap import wrap

class BogusSMTPConnection(object):
  """Instead of sending emails, print them to the console."""

  def __init__(*args, **kwargs):
    print("Initialized bogus SMTP connection")

  def open(self):
    print("Open bogus SMTP connection")

  def close(self):
    print("Close bogus SMTP connection")

  def send_messages(self, messages):
    print("Sending through bogus SMTP connection:")
    for message in messages:
      print("tFrom: %s" % message.from_email)
      print("tTo: %s" % ", ".join(message.to))
      print("tSubject: %s" % message.subject)
      print("t%s" % "nt".join(wrap(message.body)))
      print(messages)
      return len(messages)

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Provide a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class AddGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('game_name', 'game_url', 'game_price')
