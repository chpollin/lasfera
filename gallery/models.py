# gallery/models.py
from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
)
from modelcluster.fields import ParentalKey
from wagtail.snippets.models import register_snippet


def get_context(self, request):
    context = super().get_context(request)

    # Get gallery pages
    gallery_pages = GalleryDetailPage.objects.live().order_by("-first_published_at")

    # Apply theme filter if present
    theme_filter = request.GET.get("theme")
    if theme_filter:
        gallery_pages = gallery_pages.filter(themes__theme__name=theme_filter)

    # Add the pages and all available themes to context
    context["gallery_pages"] = gallery_pages
    context["themes"] = ImageTheme.objects.all()
    context["current_theme"] = theme_filter

    # Check if it's an HTMX request
    if request.headers.get("HX-Request"):
        # If it's an HTMX request, we'll render just the gallery grid portion
        self.template = "gallery/partials/gallery_grid.html"

    return context


@register_snippet
class ImageTheme(models.Model):
    """Themes for categorizing gallery images"""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
    ]

    def __str__(self):
        return self.name


class GalleryIndexPage(Page):
    """The main gallery listing page"""

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    def get_context(self, request):
        context = super().get_context(request)

        # Get gallery pages
        gallery_pages = GalleryDetailPage.objects.live().order_by("-first_published_at")

        # Apply theme filter if present
        theme_filter = request.GET.get("theme")
        if theme_filter:
            gallery_pages = gallery_pages.filter(themes__theme__name=theme_filter)

        # Add the pages and all available themes to context
        context["gallery_pages"] = gallery_pages
        context["themes"] = ImageTheme.objects.all()
        context["current_theme"] = theme_filter

        return context


class GalleryImageThemeRelationship(models.Model):
    """Intermediate model for many-to-many relationship between gallery pages and themes"""

    page = ParentalKey("GalleryDetailPage", related_name="themes")
    theme = models.ForeignKey("ImageTheme", on_delete=models.CASCADE, related_name="+")

    panels = [
        FieldPanel("theme"),
    ]


class GalleryDetailPage(Page):
    """Individual gallery image page"""

    main_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    caption = models.CharField(max_length=255, blank=True)
    description = RichTextField(blank=True)

    # Optional: Link to your existing manuscript data
    related_manuscript = models.ForeignKey(
        "manuscript.SingleManuscript",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="gallery_images",
    )

    related_folio = models.ForeignKey(
        "manuscript.Folio",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="gallery_images",
    )

    content_panels = Page.content_panels + [
        FieldPanel("main_image"),
        FieldPanel("caption"),
        FieldPanel("description"),
        InlinePanel("themes", label="Themes"),
        MultiFieldPanel(
            [
                FieldPanel("related_manuscript"),
                FieldPanel("related_folio"),
            ],
            heading="Related Manuscript Data",
        ),
    ]
