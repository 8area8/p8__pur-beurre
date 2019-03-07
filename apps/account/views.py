"""Account views."""

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from apps.login.models import Profile
from .forms import ProfileForm


@login_required()
def account(request):
    """Account view."""
    current_user = request.user
    initial = {'email': current_user.email,
               "news_letter": current_user.profile.news_letter,
               "username": current_user.username,
               'avatar': None,
               "description": current_user.profile.description}

    if request.method == 'POST':

        form = ProfileForm(request.POST, request.FILES, initial=initial)
        if form.has_changed() and form.is_valid():
            form.change_password(current_user, request)
            form.change_avatar(current_user, request)
            form.change_description(current_user, request)
            form.change_news_letter(current_user, request)

    else:
        form = ProfileForm(initial=initial)

    users = [user for user in Profile.objects.all()
             if current_user != user.user]
    return render(request, 'account.html', {"site_title": "Mon compte",
                                            "user": current_user,
                                            "users": users,
                                            "form": form})


@login_required()
def remove_avatar(request):
    """Remove_avatar view."""
    user = request.user
    user.profile.avatar.delete()
    user.save()
    messages.success(request, 'Avatar supprimé. Défaut: Gravatar.')
    return redirect("account")


def profiles(request, username=''):
    """Research a user."""
    other_user = User.objects.get(username=username)
    if other_user:
        return render(request, "profiles.html",
                      {"other_user": other_user,
                       "site_title": "Profiles"})
    else:
        return render(request, "no_profile_found.html",
                      {"site_title": "Aucun utilisateur"})
