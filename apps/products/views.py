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

from .models import Product, Substitute
from .substitutes_algo import FindSubstitutes


@staff_member_required
def full_in_database(request):
    """Full in top the database."""
    pages = int(request.GET.get("pages"))
    celery = request.GET.get("celery")
    if not celery:
        celery = False
    management.call_command("generate_products", pages=pages, celery=celery)
    messages.success(request, "Les produits ont bien été chargés.")
    return redirect('/admin/')


def research_product(request, research=None):
    """Research a product."""
    products = Product.objects.all().filter(name__icontains=research)
    if products:
        product = products[0]
        other_results = len(products) - 1
        substitutes = FindSubstitutes.run(product)
        return render(request, "results.html",
                      {"product": product,
                       "other_results": other_results,
                       "research": research,
                       "substitutes": substitutes,
                       "site_title": "Résultat"})
    else:
        return render(request, "no_products_found.html",
                      {"site_title": "Aucun produits"})


def results_list(request, research=None):
    """Get the results list."""
    page = request.GET.get('page')

    products = Product.objects.all().filter(name__icontains=research)
    book = Paginator(products, 25)

    products = book.get_page(page)
    return render(request, "results_list.html", {"products": products,
                                                 "research": research,
                                                 "site_title": "Résultats"})


def informations(request, product=None):
    """Product information page."""
    try:
        product = Product.objects.get(name=product)
    except Product.DoesNotExist:
        return render(request, "product_not_found.html")
    else:
        nutriscore_img = f"nutriscore-{product.nutriscore}.png"
        return render(request,
                      "informations.html", {"product": product,
                                            "nutriscore_img": nutriscore_img,
                                            "site_title": "Informations"})


@login_required
def save_substitute(request):
    """Save a substitute."""
    if request.method == 'POST':
        redirect_url = request.POST["next"]
        user = request.user
        base_product = request.POST["base_product"]
        base_product = Product.objects.get(name=base_product)
        product = request.POST["product"]
        product = Product.objects.get(name=product)

        for substitute in user.substitute_set.all():
            if substitute.substituted.name == product.name:
                messages.error(
                    request, "Le substitut est déjà présent dans vote liste.")
                return redirect(redirect_url)

        Substitute.objects.create(user=user, base_product=base_product,
                                  substituted=product)

        messages.success(request, "Substitut sauvegardé.")
    return redirect(redirect_url)


@login_required
def substitutes(request):
    """Show the substitutes page."""
    substitutes = request.user.substitute_set.all()
    for sub in substitutes:
        sub.nutriscore = f"nutriscore-{sub.substituted.nutriscore}.png"
    return render(request, "substitutes.html", {"substitutes": substitutes,
                                                "site_title": "Substituts"})


@login_required
def del_substitute(request):
    """Delete a substitute."""
    if request.method == 'POST':
        subname = request.POST["substitute_name"]
        username = request.POST["username"]
        substitute = Substitute.objects.get(substituted__name=subname,
                                            user__username=username)
        substitute.delete()
        messages.success(request, "Substitut supprimé.")
    return redirect('substitutes')
