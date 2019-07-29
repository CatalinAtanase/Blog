from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import (
    Post, 
    Comment, 
    Reply,
)
from .forms import CommentForm, ReplyForm
from django.contrib.auth.decorators import login_required  # function view
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages


class PostListView(ListView):
    
    model = Post
    context_object_name = 'posts'
    ordering = ['-created_at']
    # paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Welcome'
        return context

    def get_template_names(self, **kwargs):
        return 'post/home.html'


class PostDetailView(DetailView):
    
    model = Post
    context_object_name = 'post'
    ordering = ['-created_at'] 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get(self.pk_url_kwarg)
        context['comments'] = Comment.objects.filter(post=pk)
        context['comment_form'] = CommentForm()
        context['reply_form'] = ReplyForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'description', 'body']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'description', 'body']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update post'
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

    def get_success_url(self):
        return f'/accounts/profile/{self.request.user.username}/'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete'
        return context


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)                
            comment.post = post
            comment.user = request.user
            comment.save()
            
            return redirect(f'/post/{pk}#comments')

    messages.info(request, 'Please write a valid comment')
    return redirect('post_detail', pk=pk)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Comment
    fields = ['body']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Comment'
        return context

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.user:
            return True
        return False

    
# Update view made from 0
# def update_comment(request, pk, post_pk):
#     title = 'Update comment'
#     comment = get_object_or_404(Comment, pk=pk)
#     form = CommentForm(instance=comment)

#     if request.method == 'POST':
#         form = CommentForm(request.POST, instance=comment)

#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Your comment has been updated.')
            
#             return redirect(f'/post/{post_pk}#comments')
    
#     return render(request, 'post/comment_update.html', locals())


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.user:
            return True
        return False

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.get_object().post.id})

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Comment'
        return context


def add_reply_to_comment(request, pk, post_pk):
    comment =  get_object_or_404(Comment, pk=pk)

    if request.method == 'POST':
        form = ReplyForm(request.POST) 

        if form.is_valid():
            reply = form.save(commit=False)
            reply.comment = comment
            reply.user = request.user
            reply.save()

            return redirect(f'/post/{post_pk}#comments')

    messages.info(request, 'Please write a valid reply.')
    return redirect('post_detail', pk=post_pk)


class ReplyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Reply
    fields = ['body']

    def test_func(self):
        reply = self.get_object()
        return True if reply.user == self.request.user else False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update reply'
        return context


class ReplyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    
    model = Reply
    
    def test_func(self):
        return True if self.request.user == self.get_object().user else False

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.get_object().comment.post.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Reply'
        return context
    


