from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('post/add', views.PostCreateView.as_view(), name='post_create'),
    path('post/update/<pk>', views.PostUpdateView.as_view(), name='post_update'),
    path('post/delete/<pk>', views.PostDeleteView.as_view(), name='post_delete'),
]