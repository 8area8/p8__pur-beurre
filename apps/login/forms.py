"""Login form."""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class SignUpForm(UserCreationForm):
    """Specific form with intermediate email value."""

    email = forms.EmailField(
        max_length=254, help_text='Requis. Renseignez une adresse mail valide.')

    class Meta:
        """User fields."""

        model = User
        fields = ('username', 'email', 'password1', 'password2', )
