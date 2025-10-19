def sidebar_links(request):
    # Default links (for all logged-in users)
    sidebar_items = [
        {'name': 'Dashboard', 'icon': 'fa-solid fa-house', 'url_name': 'dashboard:dashboard'},
        {'name': 'Products', 'icon': 'fa-solid fa-box', 'url_name': 'product:product_list'},
        {'name': 'Categories', 'icon': 'fa-solid fa-layer-group', 'url_name': 'category:category_list'},
        {'name': 'Warehouses', 'icon': 'fa-solid fa-warehouse', 'url_name': 'warehouse:warehouse_list'},
        {'name': 'Inventory', 'icon': 'fa-solid fa-clipboard-list', 'url_name': 'inventory:inventory_list'},
        {'name': 'Sales', 'icon': 'fa-solid fa-cash-register', 'url_name': 'sales:sales_list'},
        {'name': 'Purchases', 'icon': 'fa-solid fa-cart-shopping', 'url_name': 'purchase:purchase_list'},
        {'name' :'Forecast' , 'icon': 'fa-solid fa-chart-line', 'url_name': 'forecast:forecast_dashboard'},
        {'name': 'Profile', 'icon': 'fa-solid fa-gear', 'url_name': '#'},
    ]

    # Add admin-only links
    if request.user.is_authenticated and request.user.is_staff:
        sidebar_items.extend([
            {'name': 'Suppliers', 'icon': 'fa-solid fa-truck', 'url_name': 'suppliers:supplier_list'},
            {'name': 'Users', 'icon': 'fa-solid fa-users', 'url_name': '#'},
        ])

    return {'sidebar_items': sidebar_items}
