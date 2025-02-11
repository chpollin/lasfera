from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"toponyms", views.ToponymViewSet, basename="toponyms")
router.register(r"toponym-detail", views.ToponymViewSet, basename="toponym-detail")
router.register(
    r"manuscript-detail", views.SingleManuscriptViewSet, basename="manuscript-detail"
)
urlpatterns = [
    # Core pages
    path("", views.index, name="index"),
    path("stanzas/", views.stanzas, name="stanzas"),
    # Manuscript routes
    path("manuscripts/", views.manuscripts, name="manuscripts"),
    path("manuscripts/<str:siglum>/", views.manuscript, name="manuscript"),
    path(
        "manuscripts/<str:siglum>/stanzas/",
        views.manuscript_stanzas,
        name="manuscript_stanzas",
    ),
    # Toponym routes
    path("toponyms/", views.toponyms, name="toponyms"),
    path("toponyms/<int:toponym_param>/", views.toponym, name="toponym_detail"),
    path("toponym-search/", views.search_toponyms, name="search_toponyms"),
    # IIIF viewer
    path(
        "mirador/<str:manuscript_id>/<str:page_number>/",
        views.mirador_view,
        name="mirador_view",
    ),
    # API and annotations
    path("api/", include(router.urls)),
    path("text-annotations/create/", views.create_annotation, name="create_annotation"),
]
