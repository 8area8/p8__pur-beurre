"""this application deals with autocompletion.

It needs to :
- redis
- redis python
- python requests
- Jquery autocomplete

It also uses django_webpack.
"""

from django.apps import AppConfig


class AutocompleteConfig(AppConfig):
    name = 'autocomplete'
