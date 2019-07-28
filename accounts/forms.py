from django.contrib.auth.forms import UserCreationForm
from django import forms 
from django.contrib.auth.models import User
from .models import Profile
from django.db import models
from .validators import (
    email_validator,
    username_validator,
)
from .validation_messages import ValidationMessages
from django.contrib.auth import forms as auth_forms

from django.utils.translation import gettext, gettext_lazy as _


class UserRegistrationForm(UserCreationForm):
    # Make email field unique
    User._meta.get_field('email')._unique = True

    # Overwrite error messages
    error_messages = {
        'password_mismatch': ValidationMessages.password_mismatch,
    }
    
    def clean_username(self):
        return username_validator(self.cleaned_data.get('username'))

    def clean_email(self):
        return email_validator(self.cleaned_data.get('email'))


    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]


class UserUpdateForm(forms.ModelForm):

    def clean_username(self):
        return username_validator(self.cleaned_data.get('username'), self.instance.pk)

    def clean_email(self):
        return email_validator(self.cleaned_data.get('email'), self.instance.pk)

    
    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'image',
        ]


class CustomAuthenticationForm(auth_forms.AuthenticationForm):
     error_messages = {
        'invalid_login': ValidationMessages.invalid_login,
        'inactive': ValidationMessages.inactive,
    }


class CustomPasswordChangeForm(auth_forms.PasswordChangeForm):
    error_messages = {
        'password_mismatch': ValidationMessages.password_mismatch,
        'password_incorrect': ValidationMessages.password_incorrect,
    }


class CustomResetPasswordForm(auth_forms.SetPasswordForm):
    error_messages = {
        'password_mismatch': ValidationMessages.password_mismatch,
    }
    