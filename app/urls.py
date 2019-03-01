"""App URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import importlib

from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # PERSONNAL VIEWS
    path('', include('apps.index.urls')),
    path('autocomplete/', include('apps.autocomplete.urls')),
    path('authenticate/', include('apps.login.urls')),
    path('account/', include('apps.account.urls')),
    path('products/', include('apps.products.urls')),
    # SOCIAL DJANGO
    url(r'^auth/', include('social_django.urls', namespace='social')),
]

# try:
#     django_local = importlib.import_module("app.local_settings")
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
# except ImportError:
#     pass
