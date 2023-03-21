from django.contrib import admin
from .models import *
from django.apps import apps
# Register your models here.


app_models = apps.get_app_config('LittleLemonAPI').get_models()
for model in app_models:
    model_name = model.__name__+"Admin"
    @admin.register(model)
    class ModelAdmin(admin.ModelAdmin):
        list_display = [field.name for field in model._meta.fields]

        class Meta:
            verbose_name = model.__name__

    ModelAdmin.__name__ = model_name