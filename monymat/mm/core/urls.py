__author__ = 'rajaprasanna'

from django.conf.urls import url
from core import api

urlpatterns = [

    url(r'^user/login$', api.Login.as_view(), name='login'),
    url(r'^user/logout$', api.Logout.as_view(), name='logout'),
    url(r'^user/signup$', api.Signup.as_view(), name='signup'),
]