

from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("user/", include("api.user.urls")),
    path("core/", include("api.core.urls")),
    path("dashboard/", include("api.dashboard.urls")),
    path("category/", include("api.category.urls")),
    path("subcategory/", include("api.subcategory.urls")),
    # path("product/", include("api.product.urls")),
    path("suppliers/", include("api.suppliers.urls")),
    path("product/", include("api.product.urls")),
]

