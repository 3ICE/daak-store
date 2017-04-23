from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


#fields required for signing up
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Provide a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

#field required for adding a game
class AddGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('game_name', 'game_url', 'game_price')

#fields required for editing a game
class EditGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('game_name', 'game_url', 'game_price')
