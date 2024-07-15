from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"toponyms", views.ToponymViewSet)


urlpatterns = [
    path("", views.index, name="index"),
    path("manuscripts/", views.manuscripts, name="manuscripts"),
    path("manuscripts/<str:siglum>/", views.manuscript, name="manuscript"),
    path("toponyms/", views.toponyms, name="toponyms"),
    path("toponyms/<int:id>/", views.toponym, name="toponym"),
    path("toponym-search/", views.search_toponyms, name="search_toponyms"),
    path("stanzas/", views.stanzas, name="stanzas"),
    path("api/", include(router.urls)),
]
