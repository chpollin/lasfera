from django.urls import include, path

from manuscript import views

app_name = "textannotation"

urlpatterns = [
    path(
        "text-annotations/get/<int:stanza_id>/",
        views.get_annotations,
        name="get_annotations",
    ),
    path(
        "annotation/<int:annotation_id>/", views.get_annotation, name="get_annotation"
    ),
]
