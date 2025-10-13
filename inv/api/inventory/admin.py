from django.contrib import admin
from .models import Inventory
# Register your models here.
@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'warehouse', 'quantity', 'last_updated')
    search_fields = ('product__name', 'warehouse__name')
    list_filter = ('warehouse', 'last_updated')
    ordering = ('-last_updated',)
