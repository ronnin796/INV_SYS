from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from api.core.permissions import AdminRequiredMixin
from .models import Warehouse
from .forms import WarehouseForm


class WarehouseListView(ListView):
    model = Warehouse
    template_name = 'warehouse/list.html'
    context_object_name = 'warehouses'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(location__icontains=query) |
                Q(manager__username__icontains=query)
            )
        return queryset


class WarehouseCreateView(AdminRequiredMixin, CreateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = 'warehouse/form.html'
    success_url = reverse_lazy('warehouse:warehouse_list')

    def form_valid(self, form):
        messages.success(self.request, "Warehouse created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class WarehouseUpdateView(AdminRequiredMixin, UpdateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = 'warehouse/form.html'
    success_url = reverse_lazy('warehouse:warehouse_list')

    def form_valid(self, form):
        messages.success(self.request, "Warehouse updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class WarehouseDeleteView(AdminRequiredMixin, DeleteView):
    model = Warehouse
    template_name = 'warehouse/confirm_delete.html'
    success_url = reverse_lazy('warehouse:warehouse_list')
    redirect_url = reverse_lazy('dashboard:dashboard')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Warehouse deleted successfully!")
        return super().delete(request, *args, **kwargs)
    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to perform this action.")
        return super().handle_no_permission()