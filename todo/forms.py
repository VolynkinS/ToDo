import re

from django import forms
from django.core.exceptions import ValidationError

from .models import Todo
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserRegisterFrom(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={'class': 'form-control', 'autocomplete': 'off'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password2 = forms.CharField(label='Confirm password',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control',
                                           'autocomplete': 'off'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        title = self.cleaned_data['username']
        if re.match(r'\d', title):
            raise ValidationError('Username must not start with a number.')
        return title


class UserLoginFrom(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(label='Username', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))


class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'memo', 'important']
        help_text = {'memo': 'Don\'t forget to write memo'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'memo': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 5})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Title must not start with a number!',
                                  code='invalid')
        return title
