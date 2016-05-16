__author__ = 'rajaprasanna'

from django.conf.urls import url
from core import api

urlpatterns = [

    url(r'^login$', api.Login.as_view(), name='login'),
    url(r'^logout$', api.Logout.as_view(), name='logout'),
    url(r'^signup$', api.Signup.as_view(), name='signup'),
]