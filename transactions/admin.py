from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'amount', 'status']
    search_fields = ['order__name']
    list_filter = ['status']
    list_select_related = ['order']
    autocomplete_fields = ['order']
    readonly_fields = ['source_order_id']
    ordering = ['-id']
    list_per_page = 10
