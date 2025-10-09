# views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Supplier
from .forms import SupplierForm
from django.db.models import Q
from django.contrib import messages
from api.core.permissions import AdminRequiredMixin

class SupplierListView(ListView):
    model = Supplier
    template_name = 'suppliers/list.html'
    context_object_name = 'suppliers'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(contact_email__icontains=query) |
                Q(phone_number__icontains=query)
            )
        return queryset


class SupplierCreateView(AdminRequiredMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/form.html'
    success_url = reverse_lazy('suppliers:supplier_list')

class SupplierUpdateView(AdminRequiredMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/form.html'
    success_url = reverse_lazy('suppliers:supplier_list')
    

class SupplierDeleteView(AdminRequiredMixin, DeleteView):
    model = Supplier
    template_name = 'suppliers/confirm_delete.html'
    success_url = reverse_lazy('suppliers:supplier_list')
    redirect_url = reverse_lazy('dashboard:dashboard')  # Redirect to dashboard if not authorized
