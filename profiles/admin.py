from django.contrib import admin

from orders.models import Order
from .models import User


class OrderInline(admin.TabularInline):
    model = Order
    extra = 0
    show_change_link = True


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'second_name', 'role', 'email']
    search_fields = ['name', 'second_name', 'email']
    list_filter = ['role']
    ordering = ['name', 'id']
    list_per_page = 10
    inlines = [OrderInline]
