from django.contrib import admin

# Register your models here.
from .models import Warehouse

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'manager', 'contact_number', 'created_at', 'updated_at')
    search_fields = ('name', 'location', 'manager__username')
    list_filter = ('created_at', 'updated_at')