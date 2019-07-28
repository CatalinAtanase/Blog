from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User

from .forms import UserRegistrationForm, UserUpdateForm, UserProfileForm
from .tokens import account_activation_token
from .models import Profile


def register(request):
    title = 'registration'
    # Render an empty form and if it's a post req render one with the data
    form = UserRegistrationForm()

    # Redirect logged in users
    if request.user.is_authenticated:
        messages.info(request, f'You are already logged in!')
        # 
        # Messages are stored in cookies and using redirect removes the cookie 
        # strange enough cuz down there works on form.is_valid()
        # 
        return render(request, 'accounts/profile.html')
    
    # First take care of the post req
    if request.method == 'POST':
        # Create a form and populate it with data from the req
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Prepare mail
            current_site = get_current_site(request)
            subject = f'Activate your account on {current_site}'
            message = render_to_string('accounts/email_verification.html', {
                'user': user,
                'protocol': request.scheme,
                'domain': current_site.domain,
                'site_name': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            user.email_user(subject=subject, message=message)
            
            messages.success(request, f'Your account has been created and an email has been sent. Check your email to complete the registration.')
            return redirect('/accounts/login')
    
    # Render the page
    return render(request, 'accounts/register.html', locals())


def profile(request, username):
    users_profile = get_object_or_404(User, username=username)
    title = 'profile'
    return render(request, 'accounts/profile.html', locals())

#TODO make value for form fields to be the initial data if form.is_valid fails
@login_required
def profile_update(request):
    title = 'profile'
    # Render empty forms for get
    user_form = UserUpdateForm(instance=request.user)
    profile_form = UserProfileForm(instance=request.user.profile)

     # Take care of the POST req
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated.')
            return redirect('profile')

    return render(request, 'accounts/profile_update.html', locals())

def error_404(request, exception):
    title = 'oops'
    return render(request, 'accounts/error_404.html', status=404)

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return render(request, 'accounts/activation_invalid.html')






    


