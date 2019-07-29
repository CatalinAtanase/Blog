from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


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
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.id})

class Comment(models.Model):

    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments_post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')

    def __str__(self):
        return self.body

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.post.id})


class Reply(models.Model):
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='reply_comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply_user')

    class Meta:
        verbose_name_plural = "replies"

    def __str__(self):
        return f'{self.user.username}'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.comment.post.pk})

    