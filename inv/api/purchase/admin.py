from django.contrib import admin
from .models import PurchaseOrder, PurchaseItem


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1
    readonly_fields = ('total',)
    fields = ('product', 'quantity', 'price', 'total')


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier', 'warehouse', 'reference_number', 'status', 'created_at')
    search_fields = ('reference_number', 'supplier__name', 'warehouse__name')
    list_filter = ('status', 'created_at', 'supplier', 'warehouse')
    ordering = ('-created_at',)
    inlines = [PurchaseItemInline]  # ✅ remove quotes here
