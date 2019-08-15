from django import forms
from .models import (
    Post,
    Comment,
    Reply, 
    Favorite,
    PostLike,
    CommentLike,
    ReplyLike
)


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


class FavoriteForm(forms.ModelForm):

    class Meta:
        fields = ()
        model = Favorite


class PostLikeForm(forms.ModelForm):

    class Meta:
        fields = ()
        model = PostLike


        
class CommentLikeForm(forms.ModelForm):

    class Meta:
        fields = ()
        model = CommentLike


class ReplyLikeForm(forms.ModelForm):

    class Meta:
        fields = ()
        model = ReplyLike
