from django.contrib import admin
from .models import Supplier
# Register your models here.
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_email', 'phone_number', 'address')
    search_fields = ('name', 'contact_email')
    list_filter = ('name',)