"""Account views."""

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from apps.login.models import Profile


from django import forms
from django.forms import ValidationError
from django.contrib.auth.models import Permission, User


class ProfileForm(forms.Form):
    """The account prfile form."""

    avatar = forms.FileField(
        help_text="Selectionnez une image.", required=False)

    description = forms.CharField(
        initial='Insérez une description...',
        required=False, widget=forms.Textarea)
    email = forms.EmailField(initial='', required=False, disabled=True)

    password = forms.CharField(widget=forms.PasswordInput, required=False)
    new_pass = forms.CharField(widget=forms.PasswordInput, required=False)
    confirm_new_pass = forms.CharField(
        widget=forms.PasswordInput, required=False)

    news_letter = forms.BooleanField(required=False)

    def clean_password(self):
        """Clean the password."""
        data = self.cleaned_data.get('password', "")
        if data:

            new = self.cleaned_data.get('new_pass', None)
            confirm = self.cleaned_data.get('confirm_new_pass', None)
            if new != confirm:
                raise ValidationError("Le nouveau mot de passe doit "
                                      "être identique dans les deux champs.")
        return data

    def change_password(self, user, request):
        """Check if password is set."""
        if user.social_auth.filter(provider='google-oauth2'):
            return

        password = self.cleaned_data.get('password', "")
        new_password = self.cleaned_data.get('new_pass', None)
        if not password and not new_password:
            return

        if not user.check_password(password):
            messages.error(request, 'mot de passe incorrect.')
            return

        if not new_password:
            messages.error(request, 'Veuillez entrer un nouveau mot de passe.')
            return

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'Mise à jour du mot de passe.')

    def change_avatar(self, user, request):
        """Check if avatar is set."""
        avatar = request.FILES.get("avatar")
        if not avatar:
            return

        else:
            user.profile.avatar.delete()
            user.profile.avatar = avatar
            user.save()
            messages.success(request, 'Avatar mis à jour.')

    def change_description(self, user, request):
        """Check if description is set."""
        description = self.cleaned_data.get('description', "")

        if description and description != user.profile.description:
            user.profile.description = description
            user.save()
            messages.success(request, 'Description mise à jour.')

    def change_news_letter(self, user, request):
        """Check if news_letter is set."""
        news_letter = self.cleaned_data.get('news_letter', "")

        if news_letter != user.profile.news_letter:
            user.profile.news_letter = news_letter
            if news_letter:
                user.email_user("Vous êtes désormais inscrits", "Merci !")
                messages.success(request, "Merci pour la souscription !")
            else:
                messages.success(request, "Vous êtes désinscrits. :(")
            user.save()


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
