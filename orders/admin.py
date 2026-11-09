from django.contrib import admin

from applications.models import Application
from transactions.models import Transaction
from reviews.models import Review
from .models import Order


class ApplicationInline(admin.TabularInline):
    model = Application
    extra = 0
    autocomplete_fields = ['executor']
    show_change_link = True


class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 0
    show_change_link = True


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    autocomplete_fields = ['author']
    show_change_link = True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'customer', 'budget', 'status']
    search_fields = ['name', 'customer__name', 'customer__second_name']
    list_filter = ['status', 'customer']
    list_select_related = ['customer']
    ordering = ['-id']
    list_per_page = 10
    autocomplete_fields = ['customer']
    readonly_fields = ['source_customer_id']
    inlines = [ApplicationInline, TransactionInline, ReviewInline]
