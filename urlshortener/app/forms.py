from django import forms
from .models import URL
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class URLForm(forms.ModelForm):
    class Meta:
        model = URL
        fields = ['original_url']
        widgets = {
            'original_url': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'Paste your long URL here...',
                'required': True,
            }),
        }


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'you@example.com'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Choose a username',
        })
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Create a password',
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirm your password',
        })

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your email',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your password',
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            try:
                user = User.objects.get(email=email)
                self.user = authenticate(username=user.username, password=password)
                if self.user is None:
                    raise forms.ValidationError('Invalid email or password.')
            except User.DoesNotExist:
                raise forms.ValidationError('Invalid email or password.')
        return cleaned_data

    def get_user(self):
        return self.user