"""pfinal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from museos.feeds import myFeed

#De momento login/logout en el limbo, y de momento solo pruebo el css
urlpatterns = patterns('',
    url(r'^$', 'museos.views.barra'),
    url(r'^museos/$', 'museos.views.museos'),
    url(r'^about/$','museos.views.about'),
    url(r'^museo/(\d+)$', 'museos.views.museo'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'login','museos.views.my_login'),
    url(r'logout','museos.views.my_logout'),
    url(r'registration','museos.views.my_registration'),
    url(r'^feed/rss/$',myFeed()),
    url(r'(.*)/xml$','museos.views.usuario_xml'),
    url(r'^(.*)$', 'museos.views.usuario')
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
