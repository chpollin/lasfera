from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("manuscript.urls")),
    path("accounts/", include("allauth.urls")),
    path("admin/", admin.site.urls),
    path("prose/", include("prose.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
]
