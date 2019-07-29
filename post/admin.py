from django.contrib import admin
from .models import Post, Comment, Reply

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user']
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'body', 'user', ]
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['comment', 'body']
    readonly_fields = ('created_at', 'updated_at')



