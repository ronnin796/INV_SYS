from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from api.core.permissions import AdminRequiredMixin, SuccessMessageMixin
from .models import Inventory
from .forms import InventoryForm
from api.warehouse.models import Warehouse
from api.category.models import Category
from api.subcategory.models import SubCategory


# -----------------------------------------
# Base CRUD mixin for DRYness
# -----------------------------------------
class InventoryBaseView(AdminRequiredMixin, SuccessMessageMixin):
    """Base mixin for all Inventory CRUD views."""
    model = Inventory
    form_class = InventoryForm
    template_name = 'inventory/form.html'
    success_url = reverse_lazy('inventory:inventory_list')


# -----------------------------------------
# List View
# -----------------------------------------
class InventoryListView(ListView):
    model = Inventory
    template_name = 'inventory/list.html'
    context_object_name = 'inventory_items'

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .select_related('warehouse', 'product__category', 'product__subcategory')
        )

        query = self.request.GET.get('q')
        warehouse_id = self.request.GET.get('warehouse')
        category_id = self.request.GET.get('category')
        subcategory_id = self.request.GET.get('subcategory')

        # 🔍 Search
        if query:
            queryset = queryset.filter(
                Q(product__name__icontains=query)
                | Q(warehouse__name__icontains=query)
                | Q(product__category__name__icontains=query)
                | Q(product__subcategory__name__icontains=query)
            )

        # 🏭 Filters
        if warehouse_id:
            queryset = queryset.filter(warehouse_id=warehouse_id)
        if category_id:
            queryset = queryset.filter(product__category_id=category_id)
        if subcategory_id:
            queryset = queryset.filter(product__subcategory_id=subcategory_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.request.GET.get('category')

        context.update({
            'warehouses': Warehouse.objects.all(),
            'categories': Category.objects.all(),
            'subcategories': SubCategory.objects.filter(category_id=category_id)
            if category_id else None,
        })
        return context


# -----------------------------------------
# CRUD Views (DRY!)
# -----------------------------------------
class InventoryCreateView(InventoryBaseView, CreateView):
    success_message = "Inventory item created successfully!"


class InventoryUpdateView(InventoryBaseView, UpdateView):
    success_message = "Inventory item updated successfully!"


class InventoryDeleteView(AdminRequiredMixin, DeleteView):
    model = Inventory
    template_name = 'inventory/confirm_delete.html'
    success_url = reverse_lazy('inventory:inventory_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Inventory item deleted successfully!")
        return super().delete(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to perform this action.")
        return super().handle_no_permission()
