from django import forms
from .models import URL
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class URLForm(forms.ModelForm):
    class Meta:
        model = URL
        fields = ['original_url']
        
        
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

