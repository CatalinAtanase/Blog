from django import forms
from .models import Post, Comment, Reply


class CommentForm(forms.ModelForm):

    my_default_errors = {
        'required': 'Trb sa completezi cumetre',
        'invalid': 'Enter a valid value',
    }

    body = forms.CharField(widget=forms.Textarea(attrs={'rows': 10}), error_messages=my_default_errors)


    class Meta:
        model = Comment
        fields = ('body',)


class ReplyForm(forms.ModelForm):

    my_default_errors = {
        'required': 'Trb sa completezi cumetre',
        'invalid': 'Enter a valid value',
    }

    body = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), error_messages=my_default_errors)


    class Meta:
        model = Reply
        fields = ('body',)
