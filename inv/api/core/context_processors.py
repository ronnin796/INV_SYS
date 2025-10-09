def sidebar_links(request):
    # Default links (for all logged-in users)
    sidebar_items = [
        {'name': 'Dashboard', 'icon': 'fa-solid fa-house', 'url_name': 'dashboard:dashboard'},
        {'name': 'Products', 'icon': 'fa-solid fa-box', 'url_name': '#'},
        {'name': 'Categories', 'icon': 'fa-solid fa-layer-group', 'url_name': 'category:category_list'},
        {'name': 'Orders', 'icon': 'fa-solid fa-cart-shopping', 'url_name': '#'},
        {'name': 'Profile', 'icon': 'fa-solid fa-gear', 'url_name': '#'},
    ]

    # Add admin-only links
    if request.user.is_authenticated and request.user.is_staff:
        sidebar_items.extend([
            {'name': 'Suppliers', 'icon': 'fa-solid fa-truck', 'url_name': 'suppliers:supplier_list'},
            {'name': 'Users', 'icon': 'fa-solid fa-users', 'url_name': '#'},
        ])

    return {'sidebar_items': sidebar_items}
