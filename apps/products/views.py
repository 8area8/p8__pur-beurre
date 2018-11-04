"""Products view."""

from django.shortcuts import render, redirect
from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core import management
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Product


@staff_member_required
def full_in_database(request):
    """Full in top the database."""
    management.call_command("generate_products")
    messages.success(request, "Les produits ont bien été chargés.")
    return redirect('/admin/')


@login_required
def research_product(request, research=None):
    """Research a product."""
    products = Product.objects.all().filter(name__icontains=research)
    if products:
        product = products[0]
        nutriscore_img = f"nutriscore-{product.nutriscore}.png"
        other_results = len(products) - 1
        return render(request, "results.html",
                      {"product": product,
                       "nutriscore_img": nutriscore_img,
                       "other_results": other_results,
                       "research": research}
                      )
    else:
        return render(request, "no_products_found.html")


@login_required
def results_list(request, research=None):
    """Research a product."""
    page = request.GET.get('page')

    products = Product.objects.all().filter(name__icontains=research)
    book = Paginator(products, 25)

    products = book.get_page(page)
    return render(request, "results_list.html", {"products": products,
                                                 "research": research})


@login_required
def informations(request, product=None):
    """Research a product."""
    product = Product.objects.get(name=product)
    if product:
        nutriscore_img = f"nutriscore-{product.nutriscore}.png"
        return render(request,
                      "informations.html", {"product": product,
                                            "nutriscore_img": nutriscore_img})
    else:
        return render(request, "product_not_found.html")
