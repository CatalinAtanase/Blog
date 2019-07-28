from django.contrib.auth.models import User
from django import forms
from .validation_messages import ValidationMessages
from django.contrib.auth.password_validation import MinimumLengthValidator


class MinimumLengthValidator(MinimumLengthValidator):
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise forms.ValidationError(ValidationMessages.get_password_min_length(self.min_length))
                
            
# Use pk for updating and pk none when creating a new user
def username_validator(username, pk=None):
    if User.objects.filter(username=username).exclude(pk=pk).count():
        raise forms.ValidationError(ValidationMessages.unique_user)
    
    return username

def email_validator(email, pk=None):
    if User.objects.filter(email=email).exclude(pk=pk).count():
        raise forms.ValidationError(ValidationMessages.unique_email)
    
    return email


