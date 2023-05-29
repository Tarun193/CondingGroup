from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','username', 'email','bio']


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'name', 'username', 'password1', 'password2']
