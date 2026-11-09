from django.contrib import admin

from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'executor', 'comment']
    search_fields = ['order__name', 'executor__name', 'comment']
    list_filter = ['executor']
    list_select_related = ['order', 'executor']
    autocomplete_fields = ['order', 'executor']
    readonly_fields = ['source_order_id', 'source_executor_id']
    ordering = ['-id']
    list_per_page = 10
