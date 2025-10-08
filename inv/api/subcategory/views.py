from django.shortcuts import render
from .models import SubCategory
from .forms import SubCategoryForm
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from api.category.models import Category

def subcategory_list(request , pk):
    category = get_object_or_404(Category, pk=pk)
    subcategory_list = category.subcategories.all()
    # Logic to retrieve and display categories
    return render(request, 'subcategory/list.html', {
        'categories': subcategory_list , 
        'category': category
    })

def subcategory_create(request):
    if request.method == 'POST':
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            subcategory = form.save()
            messages.success(request, "New subcategory created successfully.")
            return redirect('subcategory:subcategory_list' , pk = subcategory.category.id )  # Redirect to the category list page
    else:
        form = SubCategoryForm()
    return render(request, 'subcategory/create.html', {'form': form})


def edit_subcategory(request, pk):
    # Get the category by primary key (pk)
    item = get_object_or_404(SubCategory, pk=pk)

    # Allow only superusers to edit
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to edit categories.")
        return redirect('subcategory_list')

    if request.method == 'POST':
        form = SubCategoryForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "SubCategory updated successfully!")
            return redirect('subcategory:subcategory_list')  # Redirect to the category list page
    else:
        form = SubCategoryForm(instance=item)

    return render(request, 'subcategory/create.html', {'form': form, 'item': item})

def delete_subcategory(request, pk):
    # Get the category by primary key (pk)
    item = get_object_or_404(SubCategory, pk=pk)
    item_id = item.category.id

    # Allow only superusers to delete
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to delete categories.")
        return redirect('subcategory_list' , pk = item_id)

    # Handle POST request (actual deletion)
    if request.method == 'POST':
        item.delete()
        messages.success(request, "SubCategory deleted successfully!")
        return redirect('subcategory:subcategory_list' , pk = item_id)  # Redirect to the category list page

    # For GET request: show confirmation page
    return render(request, 'subcategory/confirm_delete.html', {'item': item})
