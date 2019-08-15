from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
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
    Favorite,
    PostLike,
    CommentLike
)
from .forms import (
    CommentForm, 
    ReplyForm, 
    FavoriteForm,
    PostLikeForm,
    CommentLikeForm
)
from django.contrib.auth.decorators import login_required  # function view
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.template.defaultfilters import pluralize


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
        if self.request.user.is_authenticated:
            context['is_favorite'] = Favorite.objects.filter(user=self.request.user).filter(post=self.get_object()).first()
        return context


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    fields = ['title', 'description', 'body']
    success_message = 'Your post was created successfully'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Post
    fields = ['title', 'description', 'body']
    success_message = 'Your post was updated successfully'

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

@login_required
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

@login_required
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

def add_favorite(request, post_pk):
    if request.method == 'POST':
        form = FavoriteForm(request.POST)

        if form.is_valid():
            postPreference = form.save(commit=False)
            postPreference.user = request.user
            postPreference.post = Post.objects.get(pk=post_pk)
            postPreference.save()

            messages.success(request, 'The post was successffuly added!')

            return redirect('favorite_list', username=request.user.username)

    form = FavoriteForm()
    return redirect('post_detail', pk=post_pk)


class FavoritesListView(ListView):

    model = Favorite
    context_object_name = 'favorites'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        context = Favorite.objects.filter(user=user)
        
        return context    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Favorites'
        context['current_page'] = get_object_or_404(User, username=self.kwargs['username']).username

        return context

    def get_template_names(self, **kwargs):
        return 'post/favorites.html'


class FavoriteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Favorite

    def test_func(self):
        return True if self.get_object().user == self.request.user else False

    def get_success_url(self):
        return reverse('favorite_list', kwargs={'username': self.request.user.username})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Remove Favorite'
        return context

# like to post with reload
# def toggle_like_to_post(request, post_pk):
#     if request.method == 'POST':

#         post_like = PostLike.objects.filter(
#             Q(user=request.user),
#             Q(post=post_pk)
#         ).first()

#         if post_like is not None:
#             post_like.delete()
#         else:
#             form = PostLikeForm(request.POST)
    
#             if form.is_valid():
#                 post_like = form.save(commit=False)
#                 post_like.user = request.user
#                 post_like.post = Post.objects.get(id=post_pk)
#                 post_like.save()

#     return redirect('/')

# like to post with ajax
def toggle_like_to_post(request):
    if request.method == 'POST':

        user = request.user
        post = Post.objects.get(id=request.POST['post'])

        post_like = PostLike.objects.filter(
            Q(user=user),
            Q(post=post)
        ).first()

        if post_like is None:
            PostLike.objects.create(
                user = user,
                post = post
            )
        else:
            post_like.delete()

        likes = PostLike.objects.filter(post=post).count()

        return HttpResponse(f'{likes} like{pluralize(likes)}')

# def toggle_like_to_comment(request, comment_pk, post_pk):
#     if request.method == 'POST':
#         comment_like = CommentLike.objects.filter(
#             Q(user=request.user),
#             Q(comment=comment_pk)
#         ).first()

#         if comment_like is not None:
#             comment_like.delete()
#         else:
#             form = CommentLikeForm(request.POST)

#             if form.is_valid():
#                 comment_like = form.save(commit=False)
#                 comment_like.user = request.user
#                 comment_like.comment = Comment.objects.get(id=comment_pk)
#                 comment_like.save()

#     return redirect(f'/post/{post_pk}#comments')

def toggle_like_to_comment(request):
    if request.method == 'POST':
        
        user = request.user
        comment = Comment.objects.get(id=request.POST['comment'])

        comment_like = CommentLike.objects.filter(
            Q(user=user),
            Q(comment=comment)
        ).first()

        if comment_like is None:
            CommentLike.objects.create(
                user=user,
                comment=comment
            )
        else:
            comment_like.delete()

        likes = CommentLike.objects.filter(comment=comment).count()
        
        return HttpResponse(f'{likes} like{pluralize(likes)}')


