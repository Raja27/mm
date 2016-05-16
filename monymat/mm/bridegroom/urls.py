__author__ = 'rajaprasanna'

from django.conf.urls import url
from . import api

urlpatterns = [
    url(r'^list$', api.BrideGroomsListApi.as_view(), name='bg_list'),
    url(r'^', api.BrideGroomsAPIView.as_view(), name='bg'),
]