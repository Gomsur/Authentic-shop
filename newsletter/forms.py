from django.forms import ModelForm
from .models import User, Profile
from django import forms

from django.contrib.auth.forms import UserCreationForm


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)




class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'aria-describedby': 'id_password1_helptext',
            'class': 'form-control'
        }),
        help_text=(
            '<ul>'
            '<li>Your password can’t be too similar to your other personal information.</li>'
            '<li>Your password must contain at least 8 characters.</li>'
            '<li>Your password can’t be a commonly used password.</li>'
            '<li>Your password can’t be entirely numeric.</li>'
            '</ul>'
        )
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'aria-describedby': 'id_password2_helptext',
            'class': 'form-control'
        }),
        help_text='<ul><li>Enter the same password as before, for verification.</li></ul>'
    )

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
