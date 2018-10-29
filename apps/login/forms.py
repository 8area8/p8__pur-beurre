"""Login form."""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    """Specific form with intermediate email value for signup."""

    email = forms.EmailField(
        max_length=254, help_text='Requis. Renseignez une adresse mail valide.')

    class Meta:
        """User fields."""

        model = User
        fields = ('username', 'email', 'password1', 'password2', )

    def clean_email(self):
        """Return the email if entered email is unique.

        Otherwise gives duplicate_email error.
        """
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse mail est déjà utilisé.")
        return email
