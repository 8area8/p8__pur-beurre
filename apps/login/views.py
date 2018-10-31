"""Login views."""

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import authenticate, login as _login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.urls import reverse

from .forms import SignUpForm
from .token import account_activation_token
from app.extended_lib.anonymous import anonymous_required


BACKEND = 'apps.login.authenticate.EmailAuthenticate'


def login(request):
    """Login view."""
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, username=email, password=password)
    if user:
        _login(request, user, backend=BACKEND)
        messages.success(request, 'Vous êtes connecté.')
        return redirect("/")
    else:
        messages.error(request, 'Email ou mot de passe incorrect.')
        return redirect('/')


@anonymous_required(redirect_url="/account/")
def signup(request):
    """Signup view."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid() and form.clean_email():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activez votre compte'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    """Activate view."""
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        _login(request, user, backend=BACKEND)
        messages.success(request, 'Vous êtes connecté.')
        return redirect(reverse('index'))
    else:
        return render(request, 'account_activation_invalid.html')


def account_activation_sent(request):
    """Email sent view."""
    return render(request, 'account_activation_sent.html')


def logout(request):
    """Log out user."""
    auth_logout(request)
    messages.success(request, 'Vous êtes déconnecté.')
    return redirect('/')
