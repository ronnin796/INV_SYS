from django.contrib import admin
from .models import SalesOrder, SalesItem


class SalesItemInline(admin.TabularInline):
    model = SalesItem
    extra = 1
    readonly_fields = ('total',)
    fields = ('product', 'quantity', 'price', 'total')


@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "status", "created_at")
    search_fields = ("reference_number", "customer__name", "status")
    list_filter = ("status", "warehouse")
    ordering = ("-created_at",)
    inlines = [SalesItemInline]

    def total_amount(self, obj):
        return obj.total
    total_amount.short_description = "Total"
