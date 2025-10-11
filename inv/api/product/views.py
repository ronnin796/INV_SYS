from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect
from .models import Product
from .forms import ProductForm
from api.core.permissions import AdminRequiredMixin  # assuming your AdminRequiredMixin is in core.mixins4py
from api.subcategory.models import SubCategory
from django.http import JsonResponse
from api.category.models import Category


class ProductListView(ListView):
    model = Product
    template_name = 'product/list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('category', 'subcategory', 'supplier')
        query = self.request.GET.get('q')
        category_id = self.request.GET.get('category')
        subcategory_id = self.request.GET.get('subcategory')

        # 🔍 Search
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(category__name__icontains=query) |
                Q(subcategory__name__icontains=query) |
                Q(supplier__name__icontains=query)
            )

        # 🧩 Filter by category and subcategory
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if subcategory_id:
            queryset = queryset.filter(subcategory_id=subcategory_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.request.GET.get('category')

        context['categories'] = Category.objects.all()
        # Load only subcategories belonging to selected category
        context['subcategories'] = SubCategory.objects.filter(category_id=category_id) if category_id else None
        return context


class ProductCreateView(AdminRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/form.html'
    success_url = reverse_lazy('product:product_list')

    def form_valid(self, form):
        messages.success(self.request, "✅ Product added successfully.")
        return super().form_valid(form)


class ProductUpdateView(AdminRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/form.html'
    success_url = reverse_lazy('product:product_list')

    def form_valid(self, form):
        messages.success(self.request, "✅ Product updated successfully.")
        return super().form_valid(form)


class ProductDeleteView(AdminRequiredMixin, DeleteView):
    model = Product
    template_name = 'product/confirm_delete.html'
    success_url = reverse_lazy('product:product_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "🗑️ Product deleted successfully.")
        return super().delete(request, *args, **kwargs)
    
def load_subcategories(request):
    category_id = request.GET.get('category')
    subcategories = SubCategory.objects.filter(category_id=category_id).order_by('name')
    subcategory_list = [{'id': sub.id, 'name': sub.name} for sub in subcategories]
    return JsonResponse(subcategory_list, safe=False)



def ajax_load_products(request):
    warehouse_id = request.GET.get('warehouse')
    subcategory_id = request.GET.get('subcategory')

    products = Product.objects.all()

    if warehouse_id:
        products = products.filter(warehouse_id=warehouse_id)

    if subcategory_id:
        products = products.filter(subcategory_id=subcategory_id)

    data = list(products.values('id', 'name'))
    return JsonResponse(data, safe=False)
