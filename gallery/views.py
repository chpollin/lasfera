from django.shortcuts import get_object_or_404, render
from gallery.models import GalleryIndexPage, ImageTheme, GalleryDetailPage


def filter_gallery(request, page_id):
    """View to handle HTMX filtering requests for the gallery."""
    page = get_object_or_404(GalleryIndexPage, id=page_id)

    # Get gallery pages
    gallery_pages = GalleryDetailPage.objects.live().order_by("-first_published_at")

    # Apply theme filter if present
    theme_filter = request.GET.get("theme")
    if theme_filter:
        gallery_pages = gallery_pages.filter(themes__theme__name=theme_filter)

    # Create context for the template
    context = {
        "gallery_pages": gallery_pages,
        "current_theme": theme_filter,
    }

    return render(request, "gallery/partials/gallery_grid.html", context)
