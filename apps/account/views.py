"""Account views."""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required()
def account(request):
    """Account view."""
    return render(request, 'account.html', {"site_title": "Mon compte"})
