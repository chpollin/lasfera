from django.urls import path
from . import views

app_name = "gallery"

urlpatterns = [
    path("filter/<int:page_id>/", views.filter_gallery, name="filter_gallery"),
]
