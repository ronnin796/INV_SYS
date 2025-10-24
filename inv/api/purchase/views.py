from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.db import transaction
from django.db.models import Q
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from api.core.permissions import AdminRequiredMixin, SuccessMessageMixin
from api.inventory.models import Inventory
from api.suppliers.models import Supplier
from api.warehouse.models import Warehouse

from .models import PurchaseOrder, PurchaseItem
from .forms import PurchaseOrderForm, PurchaseItemFormSet


def update_inventory_after_purchase(purchase_order):
    # atomic handled by caller if needed
    for item in purchase_order.items.select_related("product"):
        inventory, _ = Inventory.objects.get_or_create(
            product=item.product, warehouse=purchase_order.warehouse, defaults={"quantity": 0}
        )
        inventory.quantity = (inventory.quantity or 0) + (item.quantity or 0)
        inventory.save()


def mark_purchase_as_received(purchase, request=None):
    if purchase.status == "Received":
        if request:
            messages.info(request, f"Purchase {purchase.reference_number} already received.")
        return False

    # 🚫 Tell signal to skip this one
    purchase._skip_signal = True

    purchase.status = "Received"
    purchase.save()  # signal won't run

    update_inventory_after_purchase(purchase)  # manual update

    if request:
        messages.success(request, f"Purchase {purchase.reference_number} marked received & inventory updated.")
    return True



class PurchaseOrderFormsetMixin:
    """
    Provide items formset handling. Always call this mixin before the base view
    in MRO so its form_valid is used.
    """

    def get_supplier_id_from_request_or_instance(self, instance=None):
        supplier_id = None
        if self.request.method == "POST":
            supplier_id = self.request.POST.get("supplier") or None
        elif instance:
            supplier_id = getattr(instance.supplier, "id", None)
        return supplier_id

    def get_items_formset(self, instance=None):
        instance = instance or getattr(self, "object", None)
        supplier_id = self.get_supplier_id_from_request_or_instance(instance=instance)
        if self.request.method == "POST":
            return PurchaseItemFormSet(self.request.POST, instance=instance, form_kwargs={"supplier_id": supplier_id})
        return PurchaseItemFormSet(instance=instance, form_kwargs={"supplier_id": supplier_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items_formset"] = kwargs.get("items_formset", self.get_items_formset(instance=getattr(self, "object", None)))
        return context

    def form_valid(self, form):
        """
        Save both order and items atomically.
        """
        items_formset = self.get_items_formset(instance=getattr(self, "object", None))

        if form.is_valid() and items_formset.is_valid():
            with transaction.atomic():
                self.object = form.save()
                items_formset.instance = self.object
                items_formset.save()
            return super().form_valid(form)
        return self.form_invalid(form)


class PurchaseOrderBaseView(AdminRequiredMixin, SuccessMessageMixin):
    model = PurchaseOrder
    form_class = PurchaseOrderForm
    template_name = "purchase/form.html"
    success_url = reverse_lazy("purchase:purchase_list")


class PurchaseOrderListView(AdminRequiredMixin, ListView):
    model = PurchaseOrder
    template_name = "purchase/list.html"
    context_object_name = "purchase_orders"

    def get_queryset(self):
        qs = super().get_queryset().select_related("supplier", "warehouse")
        q = self.request.GET.get("q")
        supplier_id = self.request.GET.get("supplier")
        warehouse_id = self.request.GET.get("warehouse")
        filters = Q()
        if q:
            filters |= Q(reference_number__icontains=q) | Q(supplier__name__icontains=q) | Q(warehouse__name__icontains=q)
        if supplier_id:
            filters &= Q(supplier_id=supplier_id)
        if warehouse_id:
            filters &= Q(warehouse_id=warehouse_id)
        return qs.filter(filters)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({"suppliers": Supplier.objects.all(), "warehouses": Warehouse.objects.all()})
        return ctx


# Note MRO: formset mixin first so its form_valid runs
class PurchaseOrderCreateView(PurchaseOrderFormsetMixin, PurchaseOrderBaseView, CreateView):
    success_message = "Purchase order created successfully!"

    # no extra get() needed; get_items_formset uses None instance


class PurchaseOrderUpdateView(PurchaseOrderFormsetMixin, PurchaseOrderBaseView, UpdateView):
    success_message = "Purchase order updated successfully!"

    def get(self, request, *args, **kwargs):
        # ensure self.object exists before building context so formset binds to it
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # ensure self.object exists (UpdateView.post usually does)
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class PurchaseOrderDeleteView(AdminRequiredMixin, DeleteView):
    model = PurchaseOrder
    template_name = "purchase/confirm_delete.html"
    success_url = reverse_lazy("purchase:purchase_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Purchase order deleted successfully!")
        return super().delete(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to perform this action.")
        return super().handle_no_permission()


def mark_as_received(request, pk):
    purchase = get_object_or_404(PurchaseOrder, pk=pk)
    mark_purchase_as_received(purchase, request)
    return redirect("purchase:purchase_list")
