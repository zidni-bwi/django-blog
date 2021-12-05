from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile



class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))

    class Meta:
        model = User
        fields = ['username', 'password']


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class SignUpForm(UserCreationForm):

    username = forms.CharField(
        label='<b>Username</b>',
        help_text='<b>Username digunakan pada saat login</b>',
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'})
    )
    email = forms.EmailField(
        label='<b>Email</b>',
        max_length=100,
        help_text='<b>Gunakan email bisnis anda.</b>',
        widget=forms.TextInput(attrs={'placeholder': 'E-Mail', 'class': 'form-control'})
    )
    password1 = forms.CharField(
        label='<b>Password</b>',
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'autocomplete': 'new-password', 'class': 'form-control'}),
        help_text='<b>Use Secure Password!</b>',
    )
    password2 = forms.CharField(
        label='<b>Konfirmasi Password</b>',
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Komfirmasi Password', 'autocomplete': 'new-password', 'class': 'form-control'}),
        help_text='<b>Samakan dengan password di atas</b>',
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)
