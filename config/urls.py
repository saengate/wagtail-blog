"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
import os

from django.conf.urls import (
    url,
    include,
)
from django.contrib import admin
from django.conf import settings

from wagtail.core import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from rest_framework.authtoken.views import obtain_auth_token

from search import views as search_views
from blog.api import api_router
from blog import views


urlpatterns = [
    url('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += [
    url('django-admin/', admin.site.urls),

    url('admin/', include(wagtailadmin_urls)),
    url('documents/', include(wagtaildocs_urls)),
    url('search/$', search_views.search, name='search'),

    url('api/v2/', api_router.urls),

    url('rest-auth/', include('rest_auth.urls')),
    url('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    url('hello/', views.HelloView.as_view(), name='hello'),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.conf.urls.static import static
    from django.views.generic.base import RedirectView

    # tell gunicorn where static files are in dev mode
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL + 'images/',
        document_root=os.path.join(settings.MEDIA_ROOT, 'images'),
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=os.path.join(settings.STATIC_ROOT),
    )
    urlpatterns += [
        url('favicon.ico$', RedirectView.as_view(
            url=settings.STATIC_URL + 'blog/images/favicon.ico',
        ),
        ),
    ]

urlpatterns += [
    url('', include(wagtail_urls)),
]
