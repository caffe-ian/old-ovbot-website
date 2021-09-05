from django.contrib import admin
from django.urls import path, include
from pages.views import homepage, confirm, cfuser, psuccess, pfail, verify, login

from django.conf import settings
from django.views.static import serve
from django.conf.urls import url

app_name = "pages"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='homepage'),
    path('confirm-user/', confirm, name="confirm-user"),
    path('cannot-find-user/', cfuser, name="cannot-find-user"),
    path('purchase-success/', psuccess, name="purchase-success"),
    path('purchase-fail/', pfail, name="purchase-fail"),
    path('.well-known/pki-validation/A6085E730C40707DBAFA47AB2118475E.txt', verify, name='verify'),
    path('login/', login, name='login'),

    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
]
