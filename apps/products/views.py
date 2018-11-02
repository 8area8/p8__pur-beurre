"""Products view."""

from django.shortcuts import render, redirect
from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse

from django.contrib.admin.views.decorators import staff_member_required
from django.core import management
from django.contrib import messages


@staff_member_required
def full_in_database(request):
    """Full in top the database."""
    management.call_command("generate_products")
    messages.success(request, "Les produits ont bien été chargés.")
    return redirect('/admin/')
