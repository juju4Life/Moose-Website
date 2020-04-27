from django.contrib import admin
from .models import GroupName


@admin.register(GroupName)
class GroupNameAdmin(admin.ModelAdmin):
    ordering = ['category', 'group_name']
    search_fields = ['group_name']
