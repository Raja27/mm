__author__ = 'rajaprasanna'

from django.conf.urls import url
from . import api
from django.views.generic import TemplateView

urlpatterns = [

    url(r'^', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^bg/list$', api.BrideGroomsListApi.as_view(), name='bg_list'),
    url(r'^bg/', api.BrideGroomsAPIView.as_view(), name='bg'),

]