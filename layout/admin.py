from django.contrib import admin
from .models import HomePageImage


@admin.register(HomePageImage)
class HomePageAdmin(admin.ModelAdmin):
    pass
