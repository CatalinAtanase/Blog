from django import forms
from .models import Post

# class PostForm(forms.ModelForm):
#     # title = forms.CharField(max_length=100, label='Title')
#     # description = forms.CharField(max_length=255, label='Description', help_text='Let others know what this post is about')
#     # body = forms.CharField(widget=forms.Textarea)
    
#     class Meta:
#         model = Post
#         fields = [
#             'title',
#             'description',
#             'body',
#         ]

