from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, default='')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_user')

    def __str__(self):
        return self.title


class Comment(models.Model):

    body = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reply_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')

    def __str__(self):
        return self.user.username
        