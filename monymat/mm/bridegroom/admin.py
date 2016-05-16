__author__ = 'rajaprasanna'

from django.contrib import admin
from django.apps import apps

from bridegroom import models

class DynamicColumnAdmin(admin.ModelAdmin):
        def __init__(self, *args, **kwargs):
            super(DynamicColumnAdmin, self).__init__(*args, **kwargs)
            field_list = [i.name for i in self.model._meta.fields]
            self.list_display = field_list
            self.list_display_links = field_list


for model in apps.get_models():
    try:
        admin.site.register(model, DynamicColumnAdmin)
    except Exception as e:
        print(e)
