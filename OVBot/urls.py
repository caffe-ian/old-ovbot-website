from django.contrib import admin
from django.urls import path, include
from pages.views import homepage, dcase, dpack, propack, hpack, confirm, cfuser, psuccess, pfail

from django.conf import settings
from django.views.static import serve
from django.conf.urls import url

app_name = "pages"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='homepage'),
    path('donator-case/', dcase, name="donator-case"),
    path('donator-pack/', dpack, name="donator-pack"),
    path('pro-pack/', propack, name="pro-pack"),
    path('hacker-pack/', hpack, name="hacker-pack"),
    path('confirm-user/', confirm, name="confirm-user"),
    path('cannot-find-user/', cfuser, name="cannot-find-user"),
    path('purchase-success/', psuccess, name="purchase-success"),
    path('purchase-fail/', pfail, name="purchase-fail"),

    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
]
