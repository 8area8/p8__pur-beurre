"""Account forms."""

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django import forms
from django.forms import ValidationError


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
