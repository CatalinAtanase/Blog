from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
)
from .models import Post


class PostListView(ListView):
    
    model = Post
    context_object_name = 'posts'
    # paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Welcome'
        return context

    def get_template_names(self, **kwargs):
        return 'post/home.html'


class PostDetailView(DetailView):
    
    model = Post
    # context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

