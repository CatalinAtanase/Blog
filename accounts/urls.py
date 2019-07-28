from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .forms import (
    CustomAuthenticationForm,
    CustomPasswordChangeForm,
    CustomResetPasswordForm,
)

urlpatterns = [
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/',
         auth_views.LoginView.as_view(
             form_class=CustomAuthenticationForm,
             redirect_authenticated_user=True,
             template_name='accounts/login.html',
         ),
         name='login'
         ),
    path('logout/',
         auth_views.LogoutView.as_view(
             template_name='accounts/logout.html'
         ),
         name='logout'
         ),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(
             template_name='accounts/password_change.html',
             form_class=CustomPasswordChangeForm
         ),
         name='password_change'
         ),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='accounts/password_change_done.html'
         ),
         name='password_change_done'
         ),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             subject_template_name='accounts/password_reset_subject.txt',
             email_template_name='accounts/password_reset_email.html',
             template_name='accounts/password_reset.html'
         ),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'),
         name='password_reset_done'
         ),
    path('password_reset_confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(
             form_class=CustomResetPasswordForm,
             template_name='accounts/password_reset_confirm.html'
         ),
         name='password_reset_confirm'
         ),
    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
