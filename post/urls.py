from django.urls import path, include
from . import views

urlpatterns = [
    # Posts
    path('', views.PostListView.as_view(), name='home'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/add/', views.PostCreateView.as_view(), name='post_create'),
    path('post/update/<pk>/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/delete/<pk>/', views.PostDeleteView.as_view(), name='post_delete'),
    # Comments
    path('post/add_comment/<pk>/', views.add_comment_to_post, name='comment_create'),
    path('post/update_comment/<pk>/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('post/delete_comment/<pk>/', views.CommentDeleteView.as_view(), name='comment_delete'),
    # Replies
    path('post/add_reply/<pk>/<post_pk>/', views.add_reply_to_comment, name='reply_create'),
    path('post/update_reply/<pk>/', views.ReplyUpdateView.as_view(), name='reply_update'),
    path('post/delete_reply/<pk>/', views.ReplyDeleteView.as_view(), name='reply_delete'),
    # Favorites
    path('post/add_favorite/<post_pk>/', views.add_favorite, name='favorite_create'),
    path('post/favorites/<username>', views.FavoritesListView.as_view(), name='favorite_list'),
    path('post/delete_favorites/<pk>', views.FavoriteDeleteView.as_view(), name='favorite_delete'),
    # Post Like
    path('post/toggle_like_post/', views.toggle_like_to_post, name='toggle_like_post'),
    # Comment Like
    path('post/toggle_like_comment/', views.toggle_like_to_comment, name='toggle_like_comment'),
]