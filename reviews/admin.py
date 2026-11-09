from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'author', 'rating', 'text']
    search_fields = ['order__name', 'author__name', 'text']
    list_filter = ['rating']
    list_select_related = ['order', 'author']
    autocomplete_fields = ['order', 'author']
    readonly_fields = ['source_order_id', 'source_author_id']
    ordering = ['-id']
    list_per_page = 10
