from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.db import models
from prose.fields import RichTextField


class TextAnnotation(models.Model):
    """Stores annotations for specific text selections within a ProseField"""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    # Store the text position data
    from_pos = models.JSONField(
        help_text="ProseMirror position data for annotation start", default=dict
    )
    to_pos = models.JSONField(
        help_text="ProseMirror position data for annotation end", default=dict
    )
    selected_text = models.TextField(default="")
    annotation = RichTextField(
        help_text="Enter your annotation here", blank=True, null=True
    )

    ANNOTATION_TYPES = (
        ("note", "Editorial Note"),
        ("variant", "Textual Variant"),
        ("reference", "Cross Reference"),
    )
    annotation_type = models.CharField(
        max_length=20, choices=ANNOTATION_TYPES, default="note"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self):
        return self.selected_text
