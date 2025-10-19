from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.db import transaction
from django.db.models import Q
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from api.core.permissions import AdminRequiredMixin, SuccessMessageMixin
from api.inventory.models import Inventory
from api.warehouse.models import Warehouse
from api.customer.models import Customer

from .models import SalesOrder, SalesItem
from .forms import SalesOrderForm, SalesItemFormSet


def update_inventory_after_sale(sale_order):
    for item in sale_order.items.select_related("product"):
        inventory, _ = Inventory.objects.get_or_create(
            product=item.product, warehouse=sale_order.warehouse, defaults={"quantity": 0}
        )
        inventory.quantity = (inventory.quantity or 0) - (item.quantity or 0)
        inventory.save()


def mark_sale_as_completed(sale_order, request=None):
    if sale_order.status == "Completed":
        if request:
            messages.info(request, f"Sale {sale_order.reference_number or sale_order.id} already completed.")
        return False
    sale_order.status = "Completed"
    sale_order.save()
    update_inventory_after_sale(sale_order)
    if request:
        messages.success(request, f"Sale {sale_order.reference_number or sale_order.id} marked completed & inventory updated.")
    return True


class SalesOrderFormsetMixin:
    """
    Handle items formset for SalesOrder. Must be first in MRO.
    """

    def get_warehouse_id_from_request_or_instance(self, instance=None):
        warehouse_id = None
        if self.request.method == "POST":
            warehouse_id = self.request.POST.get("warehouse") or None
        elif instance and instance.warehouse:
            warehouse_id = getattr(instance.warehouse, "id", None)
        return warehouse_id


    def get_items_formset(self, instance=None):
        instance = instance or getattr(self, "object", None)
        warehouse_id = self.get_warehouse_id_from_request_or_instance(instance=instance)
        if self.request.method == "POST":
            return SalesItemFormSet(
            self.request.POST, 
            instance=instance, 
            form_kwargs={"warehouse_id": warehouse_id}
        )
        return SalesItemFormSet(
        instance=instance, 
        form_kwargs={"warehouse_id": warehouse_id}
    )


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items_formset"] = kwargs.get(
            "items_formset", self.get_items_formset(instance=getattr(self, "object", None))
        )
        return context

    def form_valid(self, form):
        items_formset = self.get_items_formset(instance=getattr(self, "object", None))
        if form.is_valid() and items_formset.is_valid():
            with transaction.atomic():
                self.object = form.save()
                items_formset.instance = self.object
                items_formset.save()
            return super().form_valid(form)
        return self.form_invalid(form)


class SalesOrderBaseView(AdminRequiredMixin, SuccessMessageMixin):
    model = SalesOrder
    form_class = SalesOrderForm
    template_name = "sales/form.html"
    success_url = reverse_lazy("sales:sales_list")


class SalesOrderListView(AdminRequiredMixin, ListView):
    model = SalesOrder
    template_name = "sales/list.html"
    context_object_name = "sales_orders"

    def get_queryset(self):
        qs = super().get_queryset().select_related("customer", "warehouse")
        q = self.request.GET.get("q")
        customer_id = self.request.GET.get("customer")
        warehouse_id = self.request.GET.get("warehouse")
        filters = Q()
        if q:
            filters |= Q(reference_number__icontains=q) | Q(customer__name__icontains=q) | Q(warehouse__name__icontains=q)
        if customer_id:
            filters &= Q(customer_id=customer_id)
        if warehouse_id:
            filters &= Q(warehouse_id=warehouse_id)
        return qs.filter(filters)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({"customers": Customer.objects.all(), "warehouses": Warehouse.objects.all()})
        return ctx


class SalesOrderCreateView(SalesOrderFormsetMixin, SalesOrderBaseView, CreateView):
    success_message = "Sales order created successfully!"


class SalesOrderUpdateView(SalesOrderFormsetMixin, SalesOrderBaseView, UpdateView):
    success_message = "Sales order updated successfully!"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class SalesOrderDeleteView(AdminRequiredMixin, DeleteView):
    model = SalesOrder
    template_name = "sales/confirm_delete.html"
    success_url = reverse_lazy("sales:sales_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Sales order deleted successfully!")
        return super().delete(request, *args, **kwargs)


def mark_as_completed(request, pk):
    sale_order = get_object_or_404(SalesOrder, pk=pk)
    mark_sale_as_completed(sale_order, request)
    return redirect("sales:sales_list")
