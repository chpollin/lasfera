from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("manuscript.urls")),
    path("accounts/", include("allauth.urls")),
    path("admin/", admin.site.urls),
    path("_nested_admin/", include("nested_admin.urls")),
    path("prose/", include("prose.urls")),
]
