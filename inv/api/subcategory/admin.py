from django.contrib import admin
from .models import SubCategory
# Register your models here.
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)