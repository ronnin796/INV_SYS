from django.shortcuts import render
from .models import Category
from .forms import CategoryForm
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

def category_list(request):
    category_list = Category.objects.all()
    # Logic to retrieve and display categories
    return render(request, 'category/list.html', {
        'categories': category_list
    })

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New category created successfully.")
            return redirect('category_list')  # Redirect to the category list page
    else:
        form = CategoryForm()
    return render(request, 'category/create.html', {'form': form})


def edit_category(request, pk):
    # Get the category by primary key (pk)
    item = get_object_or_404(Category, pk=pk)

    # Allow only superusers to edit
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to edit categories.")
        return redirect('categories_list')

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully!")
            return redirect('category:category_list')  # Redirect to the category list page
    else:
        form = CategoryForm(instance=item)

    return render(request, 'category/create.html', {'form': form, 'item': item})

def delete_category(request, pk):
    # Get the category by primary key (pk)
    item = get_object_or_404(Category, pk=pk)

    # Allow only superusers to delete
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to delete categories.")
        return redirect('categories_list')

    # Handle POST request (actual deletion)
    if request.method == 'POST':
        item.delete()
        messages.success(request, "Category deleted successfully!")
        return redirect('category:category_list')  # Redirect to the category list page

    # For GET request: show confirmation page
    return render(request, 'category/confirm_delete.html', {'item': item})
