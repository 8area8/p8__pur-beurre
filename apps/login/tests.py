"""Login tests.

TODO: test the social auth logins.
"""

from django.test import TestCase
from django.test import Client
from django.contrib import auth
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse

from .token import account_activation_token


class LoginTestCase(TestCase):
    """Login tests class."""

    def setUp(self):
        """Set up function."""
        self.client = Client()
        User.objects.create_user(username="Foo", email="bar@example.com",
                                 password="super-secret")
        self.good_log = {"email": "bar@example.com",
                         "password": "super-secret"}
        self.bad_log = {"email": "foo@example.com", "password": "foo-secret"}
        self.url = '/authenticate/login'

    def test_logged_in(self):
        """Test login function."""
        self.client.post(self.url, self.good_log)
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_not_logged_in(self):
        """Test login function."""
        self.client.post(self.url, self.bad_log)
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_status_code_and_url(self):
        """Test login function."""
        response = self.client.post(self.url, self.bad_log)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")
        response = self.client.post(self.url, self.good_log)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_message_logged_in(self):
        """Test login function."""
        response = self.client.post(self.url, self.good_log)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Vous êtes connecté.')

    def test_message_not_logged_in(self):
        """Test login function."""
        response = self.client.post(self.url, self.bad_log)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Email ou mot de passe incorrect.')


class SignupTestCase(TestCase):
    """Signup tests class.

    TODO: test email sent.
    """

    def setUp(self):
        """Set up function."""
        self.client = Client()
        self.url = '/authenticate/signup'
        self.good_post = {"username": "foo", "email": "foo@example.com",
                          "password1": "vrnvrnvrn", "password2": "vrnvrnvrn"}
        self.wrong_email = {"username": "bar", "email": "foo@example.com",
                            "password1": "vrnvrnvrn", "password2": "vrnvrnvrn"}
        self.wrong_name = {"username": "foo", "email": "bar@example.com",
                           "password1": "vrnvrnvrn", "password2": "vrnvrnvrn"}

    def test_GET_request(self):
        """Test login function."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'signup.html')

    def test_good_POST_request(self):
        """Test login function."""
        response = self.client.post(self.url, self.good_post)
        user = User.objects.all()[0]
        self.assertEqual(response.status_code, 302)
        self.assertTrue(user)
        self.assertFalse(user.is_active)
        self.assertRedirects(
            response, '/authenticate/account_activation_sent/')

    def test_wrong_email_POST_request(self):
        """Test login function."""
        User.objects.create_user(username="bar", email="foo@example.com",
                                 password="vrnvrnvrn")
        response = self.client.post(self.url, self.wrong_email)
        self.assertEqual(len(User.objects.all()), 1)
        self.assertTemplateUsed(response, 'signup.html')

    def test_wrong_name_POST_request(self):
        """Test login function."""
        User.objects.create_user(username="foo", email="foo@example.com",
                                 password="vrnvrnvrn")
        response = self.client.post(self.url, self.wrong_name)
        self.assertEqual(len(User.objects.all()), 1)
        self.assertTemplateUsed(response, 'signup.html')


class ActivateTestCase(TestCase):
    """Activate tests class."""

    def setUp(self):
        """Set up function."""
        self.client = Client()
        self.url = '/authenticate/activate/'

    def test_wrong_request(self):
        """Test login function."""
        response = self.client.get(f"{self.url}foo/bar/")
        self.assertTemplateUsed(response, 'account_activation_invalid.html')

    def test_good_request(self):
        """Test login function."""
        user = User.objects.create_user(username="foo",
                                        email="foo@example.com",
                                        password="vrnvrnvrn")
        user.is_active = False
        user.save()
        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        token = account_activation_token.make_token(user)
        response = self.client.get(reverse("activate", args=[uid, token]))
        self.assertRedirects(response, "/", status_code=302)
        user = User.objects.all()[0]
        self.assertTrue(user.is_active)
        self.assertTrue(user.profile.email_confirmed)
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
