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


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_favorites')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_favorites')

    class Meta:
        unique_together = ['user', 'post']


class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_who_liked_post')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_liked')


    class Meta:
        unique_together = ['user', 'post']
        verbose_name_plural = 'Post likes'
        verbose_name = 'Post like'


class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_who_liked_comment')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_liked')

    class Meta:
        unique_together = ['user', 'comment']
        verbose_name_plural = 'Comment likes'
        verbose_name = 'Comment like'


class ReplyLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_who_liked_reply')
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, related_name='reply_liked')

    
    class Meta:
        unique_together = ['user', 'reply']
        verbose_name = 'Reply Like'
        verbose_name_plural = 'Reply likes'