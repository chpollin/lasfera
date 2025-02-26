import json
import logging
import os
import random
import re
from collections import defaultdict
from html import unescape
from urllib.parse import urlparse

import requests
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db.models import Q
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import DetailView
from rest_framework import viewsets

from manuscript.models import (
    Folio,
    Location,
    LocationAlias,
    SingleManuscript,
    Stanza,
    StanzaTranslated,
)
from manuscript.serializers import SingleManuscriptSerializer, ToponymSerializer
from pages.models import AboutPage, SitePage
from textannotation.models import TextAnnotation

logger = logging.getLogger(__name__)


def get_manifest_data(manifest_url):
    """Fetch and cache IIIF manifest data."""
    cache_key = f"iiif_manifest_{manifest_url}"
    cached_data = cache.get(cache_key)

    if cached_data:
        return cached_data

    # Fetch and cache for 24 hours if not in cache
    response = requests.get(manifest_url)
    response.raise_for_status()
    manifest_data = response.json()
    cache.set(cache_key, manifest_data, 60 * 60 * 24)

    return manifest_data


def manuscript_stanzas(request, siglum):
    """View for displaying stanzas of a specific manuscript"""
    manuscript = get_object_or_404(SingleManuscript, siglum=siglum)
    folios = manuscript.folio_set.all()
    has_known_folios = folios.exists()

    # Get folios for this manuscript
    folios = manuscript.folio_set.all()

    # Get stanzas that appear in these folios
    stanzas = Stanza.objects.filter(folios__in=folios).distinct()
    translated_stanzas = StanzaTranslated.objects.filter(stanza__in=stanzas).distinct()

    # Process stanzas into books structure
    books = process_stanzas(stanzas)
    translated_books = process_stanzas(translated_stanzas, is_translated=True)

    # Build paired books structure
    paired_books = {}
    for book_number, stanza_dict in books.items():
        paired_books[book_number] = []
        current_folio = None

        for stanza_number, original_stanzas in stanza_dict.items():
            translated_stanza_group = translated_books.get(book_number, {}).get(
                stanza_number, []
            )

            stanza_group = {
                "original": original_stanzas,
                "translated": translated_stanza_group,
            }

            # Add folio information
            if original_stanzas:
                stanza_folios = original_stanzas[0].folios.order_by("folio_number")
                if stanza_folios.exists() and (
                    current_folio is None or stanza_folios.first() != current_folio
                ):
                    current_folio = stanza_folios.first()
                    stanza_group["new_folio"] = True
                    stanza_group["show_viewer"] = True

            paired_books[book_number].append(stanza_group)

    # Get all manuscripts for the dropdown
    manuscripts = SingleManuscript.objects.all()

    return render(
        request,
        "stanzas.html",
        {
            "paired_books": paired_books,
            "manuscripts": manuscripts,
            "default_manuscript": manuscript,
            "has_known_folios": has_known_folios,
            "manuscript": {
                "iiif_url": manuscript.iiif_url if manuscript.iiif_url else None
            },
            "folios": folios,
        },
    )


def manuscript_stanzas(request, siglum):
    """View for displaying stanzas of a specific manuscript"""
    manuscript = get_object_or_404(SingleManuscript, siglum=siglum)

    # Get all stanzas first
    stanzas = (
        Stanza.objects.all()
        .prefetch_related("folios", "annotations")
        .order_by("stanza_line_code_starts")
    )
    translated_stanzas = (
        StanzaTranslated.objects.all()
        .prefetch_related("annotations")
        .order_by("stanza_line_code_starts")
    )

    # Get folios for this manuscript (if any)
    folios = manuscript.folio_set.all()
    has_folios = folios.exists()

    # Process stanzas into books structure
    books = process_stanzas(stanzas)
    translated_books = process_stanzas(translated_stanzas, is_translated=True)

    # Build paired books structure
    paired_books = {}
    for book_number, stanza_dict in books.items():
        paired_books[book_number] = []
        current_folio = None

        for stanza_number, original_stanzas in stanza_dict.items():
            translated_stanza_group = translated_books.get(book_number, {}).get(
                stanza_number, []
            )

            stanza_group = {
                "original": original_stanzas,
                "translated": translated_stanza_group,
            }

            # Only add folio information if the manuscript has folios
            if has_folios and original_stanzas:
                stanza_folios = (
                    original_stanzas[0]
                    .folios.filter(manuscript=manuscript)
                    .order_by("folio_number")
                )
                if stanza_folios.exists() and (
                    current_folio is None or stanza_folios.first() != current_folio
                ):
                    current_folio = stanza_folios.first()
                    stanza_group["new_folio"] = True
                    stanza_group["show_viewer"] = True

            paired_books[book_number].append(stanza_group)

    # Get all manuscripts for the dropdown
    manuscripts = SingleManuscript.objects.all()

    return render(
        request,
        "stanzas.html",
        {
            "paired_books": paired_books,
            "manuscripts": manuscripts,
            "default_manuscript": manuscript,
            "manuscript": {
                "iiif_url": manuscript.iiif_url if manuscript.iiif_url else None
            },
            "folios": folios,
        },
    )


@require_POST
@ensure_csrf_cookie
def create_annotation(request):
    try:
        if not request.headers.get("X-Requested-With") == "XMLHttpRequest":
            raise ValueError("AJAX required")

        # Get required fields
        object_id = request.POST.get("stanza_id")
        selected_text = request.POST.get("selected_text")
        annotation_text = request.POST.get("annotation")
        annotation_type = request.POST.get("annotation_type")
        model_type = request.POST.get("model_type", "stanza")

        # Validate required fields
        if not all([object_id, selected_text, annotation_text, annotation_type]):
            missing_fields = [
                field
                for field, value in {
                    "stanza_id": object_id,
                    "selected_text": selected_text,
                    "annotation": annotation_text,
                    "annotation_type": annotation_type,
                }.items()
                if not value
            ]
            logger.error(f"Missing required fields: {missing_fields}")
            return JsonResponse(
                {
                    "success": False,
                    "error": f"Missing required fields: {', '.join(missing_fields)}",
                },
                status=400,
            )

        # Get the appropriate model and object
        if model_type == "stanzatranslated":
            content_type = ContentType.objects.get_for_model(StanzaTranslated)
            annotated_object = get_object_or_404(StanzaTranslated, id=object_id)
        else:
            content_type = ContentType.objects.get_for_model(Stanza)
            annotated_object = get_object_or_404(Stanza, id=object_id)

        # Create the annotation
        annotation = TextAnnotation.objects.create(
            content_type=content_type,
            object_id=object_id,
            selected_text=selected_text,
            annotation=annotation_text,
            annotation_type=annotation_type,
            from_pos=request.POST.get("from_pos"),
            to_pos=request.POST.get("to_pos"),
        )

        return JsonResponse(
            {
                "success": True,
                "annotation_id": annotation.id,
                "message": "Annotation saved successfully",
            }
        )

    except Exception as e:
        logger.exception("Error creating annotation")
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@require_GET
def get_annotations(request, stanza_id):
    try:
        stanza = Stanza.objects.get(id=stanza_id)
        annotations = TextAnnotation.objects.filter(
            content_type=ContentType.objects.get_for_model(Stanza), object_id=stanza.id
        )

        return JsonResponse(
            [
                {
                    "id": ann.id,
                    "selected_text": ann.selected_text,
                    "annotation": ann.annotation,
                    "annotation_type": ann.annotation_type,
                    "from_pos": ann.from_pos,
                    "to_pos": ann.to_pos,
                }
                for ann in annotations
            ],
            safe=False,
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def get_annotation(request, annotation_id):
    try:
        annotation = get_object_or_404(TextAnnotation, id=annotation_id)

        data = {
            "id": annotation.id,
            "selected_text": annotation.selected_text,
            "annotation": annotation.annotation,
            "annotation_type": annotation.get_annotation_type_display(),
        }

        return JsonResponse(data)

    except TextAnnotation.DoesNotExist:
        logger.error(f"Annotation {annotation_id} not found")
        return JsonResponse({"error": "Annotation not found"}, status=404)
    except Exception as e:
        logger.error(f"Error retrieving annotation: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)


def process_stanzas(stanzas, is_translated=False):
    books = defaultdict(lambda: defaultdict(list))
    for stanza in stanzas:
        book_number = int(stanza.stanza_line_code_starts.split(".")[0])
        stanza_number = int(stanza.stanza_line_code_starts.split(".")[1])

        if is_translated:
            stanza.unescaped_stanza_text = unescape(stanza.stanza_text)
        else:
            stanza.unescaped_stanza_text = unescape(stanza.stanza_text)

        books[book_number][stanza_number].append(stanza)

    return {k: dict(v) for k, v in books.items()}


def index(request: HttpRequest):
    from pages.models import HomeIntroduction

    intro = HomeIntroduction.objects.first()

    # Prefetch image URLs
    image_directory = "images/home/"
    static_dir = os.path.join(settings.STATIC_ROOT, image_directory)
    if not os.path.exists(static_dir):
        static_dir = None
        for static_dir_path in settings.STATICFILES_DIRS:
            potential_dir = os.path.join(static_dir_path, image_directory)
            if os.path.exists(potential_dir):
                static_dir = potential_dir
                break

    image_urls = []
    if static_dir:
        images = [
            f
            for f in os.listdir(static_dir)
            if os.path.isfile(os.path.join(static_dir, f))
        ]
        for image in images:
            image_urls.append(os.path.join(settings.STATIC_URL, image_directory, image))

    # Shuffle the image URLs to simulate randomness
    random.shuffle(image_urls)

    context = {
        "manuscript_images": image_urls,
        "intro": intro,  # via Wagtail
        "nav_items": [
            {
                "name": "Edition",
                "url": "reverse('stanzas')",
                "thumbnail": "/static/images/home/Wellcome230 p44.png",
            },
            {
                "name": "Gazetteer",
                "url": "reverse('toponyms')",
                "thumbnail": "/static/images/home/BNCF CSopp2618 M1B.png",
            },
            {
                "name": "Tradition",
                "url": "reverse('manuscripts')",
                "thumbnail": "/static/images/home/BNCF Mag956 cosmos.png",
            },
            {
                "name": "Resources",
                "url": "",
                "thumbnail": "/static/images/home/Basel CL194 p59.png",
            },
            {
                "name": "Gallery",
                "url": "",
                "thumbnail": "/static/images/home/NYPL f1v ship.png",
            },
            {
                "name": "About",
                "url": "/about/",
                "thumbnail": "/static/images/home/Oxford74 Jerusalem.png",
            },
        ],
    }
    return render(request, "index.html", context)


def about(request):
    about_page = AboutPage.objects.live().first()

    return render(
        request,
        "pages/about_page.html",
        {
            "about_page": about_page,
        },
    )


def education(request):
    education_page = (
        SitePage.objects.live().filter(title="La Sfera in the Classroom").first()
    )

    return render(
        request,
        "pages/site_page.html",
        {
            "page": education_page,
        },
    )


def data(request):
    data_page = SitePage.objects.live().filter(title="Data").first()

    return render(
        request,
        "pages/site_page.html",
        {
            "page": data_page,
        },
    )


def talks(request):
    talks_page = SitePage.objects.live().filter(title="Talks and Presentations").first()

    return render(
        request,
        "pages/site_page.html",
        {
            "page": talks_page,
        },
    )


def mirador_view(request, manuscript_id, page_number):
    try:
        manuscript = SingleManuscript.objects.get(id=manuscript_id)
    except SingleManuscript.DoesNotExist:
        manuscript = SingleManuscript.objects.get(siglum="Urb1")

    if not manuscript.iiif_url:
        manuscript = SingleManuscript.objects.get(siglum="Urb1")

    try:
        get_manifest_data(manuscript.iiif_url)
    except requests.RequestException:
        # Fallback to default manuscript if manifest can't be fetched
        manuscript = SingleManuscript.objects.get(siglum="Urb1")

    return render(
        request,
        "manuscript/mirador.html",
        {
            "manifest_url": manuscript.iiif_url,
        },
    )


def get_canvas_url_for_folio(manuscript_manifest, folio):
    """
    Find the correct canvas URL from the manifest for a given folio
    """
    folio_label = folio.folio_number

    # Find the matching canvas in the manifest
    for canvas in manuscript_manifest["sequences"][0]["canvases"]:
        if canvas["label"].lower() == folio_label.lower():
            return canvas["@id"]

    return None


def stanzas(request: HttpRequest):
    folios = Folio.objects.all()
    stanzas = (
        Stanza.objects.prefetch_related("annotations")
        .all()
        .order_by("stanza_line_code_starts")
    )

    translated_stanzas = (
        StanzaTranslated.objects.prefetch_related("annotations")
        .all()
        .order_by("stanza_line_code_starts")
    )
    manuscripts = SingleManuscript.objects.all()
    default_manuscript = SingleManuscript.objects.get(siglum="Urb1")

    books = process_stanzas(stanzas)
    translated_books = process_stanzas(translated_stanzas)

    # Group stanzas by folio within each book
    paired_books = {}
    for book_number, stanza_dict in books.items():
        paired_books[book_number] = []
        current_folio = None

        for stanza_number, original_stanzas in stanza_dict.items():
            # Get corresponding translated stanzas
            translated_stanza_group = translated_books.get(book_number, {}).get(
                stanza_number, []
            )

            # Add folio information
            stanza_group = {
                "original": original_stanzas,
                "translated": translated_stanza_group,
            }

            # Check if this is a new folio by looking at the first stanza's folios
            if original_stanzas:
                # Get the first stanza's folios ordered by folio_number
                stanza_folios = original_stanzas[0].folios.order_by("folio_number")

                # If the stanza has any folios and the current folio has changed
                if stanza_folios.exists() and (
                    current_folio is None or stanza_folios.first() != current_folio
                ):
                    current_folio = stanza_folios.first()
                    stanza_group["new_folio"] = True
                    stanza_group["show_viewer"] = (
                        True  # Only show viewer for new folios
                    )
                    # Optionally add information about all folios this stanza appears on
                    stanza_group["folios"] = list(
                        stanza_folios.values_list("folio_number", flat=True)
                    )
                else:
                    stanza_group["new_folio"] = False

            paired_books[book_number].append(stanza_group)
    # paired_books = {}
    # for book_number, stanza_dict in books.items():
    #     paired_books[book_number] = []
    #     current_folio = None
    #
    #     for stanza_number, original_stanzas in stanza_dict.items():
    #         # Get corresponding translated stanzas
    #         translated_stanza_group = translated_books.get(book_number, {}).get(
    #             stanza_number, []
    #         )
    #
    #         # Add folio information
    #         stanza_group = {
    #             "original": original_stanzas,
    #             "translated": translated_stanza_group,
    #         }
    #
    #         # Check if this is a new folio
    #         if original_stanzas and original_stanzas[0].related_folio != current_folio:
    #             current_folio = original_stanzas[0].related_folio
    #             stanza_group["new_folio"] = True
    #             stanza_group["show_viewer"] = True  # Only show viewer for new folios
    #         else:
    #             stanza_group["new_folio"] = False
    #
    #         paired_books[book_number].append(stanza_group)
    #
    manuscript_data = {
        "iiif_url": (
            default_manuscript.iiif_url
            if hasattr(default_manuscript, "iiif_url")
            else None
        )
    }

    return render(
        request,
        "stanzas.html",
        {
            "paired_books": paired_books,
            "manuscripts": manuscripts,
            "default_manuscript": default_manuscript,
            "manuscript": manuscript_data,
            "folios": folios,
        },
    )


class ManuscriptViewer(DetailView):
    model = Stanza
    template_name = "manuscript/viewer.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stanza = self.get_object()

        if stanza.related_folio:
            manuscript = stanza.get_manuscript()

            related_stanzas = (
                Stanza.objects.filter(related_folio=stanza.related_folio)
                .exclude(id=stanza.id)
                .order_by("stanza_line_code_starts")
            )

            context.update(
                {
                    "manifest_url": manuscript.iiif_url if manuscript else None,
                    "canvas_id": (
                        stanza.related_folio.get_canvas_id()
                        if stanza.related_folio
                        else None
                    ),
                    "related_stanzas": related_stanzas,
                    "folio_number": stanza.related_folio.number,
                    "line_range": {
                        "start": stanza.parse_line_code(stanza.stanza_line_code_starts),
                        "end": stanza.parse_line_code(stanza.stanza_line_code_ends),
                    },
                }
            )

            return context


def manuscripts(request: HttpRequest):
    manuscript_objs = SingleManuscript.objects.all()
    return render(request, "manuscripts.html", {"manuscripts": manuscript_objs})


def manuscript(request: HttpRequest, siglum: str):
    get_manuscript = get_object_or_404(
        SingleManuscript.objects.select_related("library").prefetch_related(
            "codex_set", "textdecoration_set", "editorialstatus_set"
        ),
        siglum=siglum,
    )

    # Get folios and create custom sort
    def folio_sort_key(folio):
        # Extract number and suffix from folio_number
        # Handle potential missing or malformed folio numbers
        if not folio.folio_number:
            return (float("inf"), "z")  # Put empty/null values at the end

        # Find the number part
        import re

        number_match = re.match(r"(\d+)", folio.folio_number)
        if not number_match:
            return (float("inf"), "z")

        number = int(number_match.group(1))

        # Get the suffix (r or v), default to 'z' if neither
        suffix = folio.folio_number[-1].lower()
        # Make 'v' sort before 'r' by converting to sorting value
        suffix_val = {"v": "a", "r": "b"}.get(suffix, "z")

        return (number, suffix_val)

    # Get folios and sort them
    folios = sorted(get_manuscript.folio_set.all(), key=folio_sort_key)

    # Rest of your existing code for handling locations...
    for folio in folios:
        location_aliases = LocationAlias.objects.filter(folios=folio).select_related(
            "location"
        )
        locations = {alias.location for alias in location_aliases}

        folio.related_locations = []
        for location in locations:
            primary_alias = location_aliases.filter(location=location).first()
            display_name = (
                primary_alias.placename_modern
                or primary_alias.placename_from_mss
                or location.name
                or location.modern_country
                or ""
            ).strip()

            folio.related_locations.append(
                {
                    "location": location,
                    "alias": primary_alias,
                    "display_name": display_name,
                    "sort_name": display_name.lower(),
                }
            )

        folio.related_locations.sort(key=lambda x: x["sort_name"])

    return render(
        request,
        "manuscript_single.html",
        {
            "manuscript": get_manuscript,
            "folios": folios,
            "iiif_manifest": get_manuscript.iiif_url,
        },
    )


# def manuscript(request: HttpRequest, siglum: str):
#     get_manuscript = get_object_or_404(SingleManuscript, siglum=siglum)
#     folios = get_manuscript.folio_set.prefetch_related("locations_mentioned").all()
#
#     # Fetch related LocationAlias objects for each location mentioned in the folios
#     for folio in folios:
#         for location in folio.locations_mentioned.all():
#             alias = (
#                 LocationAlias.objects.filter(location=location)
#                 .values(
#                     "placename_modern",
#                     "placename_from_mss",
#                 )
#                 .first()
#             )
#             location.alias = alias
#
#     return render(
#         request,
#         "manuscript_single.html",
#         {
#             "manuscript": get_manuscript,
#             "folios": folios,
#             "iiif_manifest": get_manuscript.iiif_url,
#         },
#     )


def toponyms(request: HttpRequest):
    # Get unique and sorted LocationAlias objects based on placename_modern
    toponym_alias_objs = (
        Location.objects.exclude(placename_id=None)
        .exclude(placename_id="")
        .values("name", "placename_id", "id")
        .distinct()
        .order_by("name")
    )
    return render(
        request, "gazetteer/gazetteer_index.html", {"aliases": toponym_alias_objs}
    )


def toponym(request: HttpRequest, placename_id: str):
    filtered_toponym = get_object_or_404(Location, placename_id=placename_id)
    filtered_manuscripts = SingleManuscript.objects.filter(
        folio__locations_mentioned=filtered_toponym.id
    ).distinct()
    filtered_folios = filtered_toponym.folio_set.all()
    filtered_linecodes = filtered_toponym.linecode_set.all()

    filtered_manuscripts = SingleManuscript.objects.filter(
        folio__locations_mentioned=filtered_toponym.id
    ).distinct()

    manuscripts_with_iiif = filtered_manuscripts.exclude(
        Q(iiif_url__isnull=True) | Q(iiif_url="")
    ).values_list("siglum", "iiif_url")

    iiif_urls = dict(manuscripts_with_iiif)

    iiif_manifest = {
        siglum: get_manifest_data(url) for siglum, url in manuscripts_with_iiif
    }

    # First get aliases with related data
    aliases = filtered_toponym.locationalias_set.all().prefetch_related(
        "manuscripts", "folios"
    )

    # Then process aggregations
    aggregated_aliases = {
        "name": filtered_toponym.name,
        "aliases": [
            {
                "placename_alias": alias.placename_alias,
                "manuscripts": alias.manuscripts.all(),
                "folios": alias.folios.all(),
            }
            for alias in aliases
        ],
        "placename_moderns": [],
        "placename_standardizeds": [],
        "placename_from_msss": [],
        "placename_ancients": [],
    }

    # Process aggregations
    for alias in aliases:
        if alias.placename_modern:
            aggregated_aliases["placename_moderns"].extend(
                name.strip() for name in alias.placename_modern.split(",")
            )
        if alias.placename_standardized:
            aggregated_aliases["placename_standardizeds"].extend(
                name.strip() for name in alias.placename_standardized.split(",")
            )
        if alias.placename_from_mss:
            aggregated_aliases["placename_from_msss"].extend(
                name.strip() for name in alias.placename_from_mss.split(",")
            )
        if alias.placename_ancient:
            aggregated_aliases["placename_ancients"].extend(
                name.strip() for name in alias.placename_ancient.split(",")
            )

    # After aliases are processed, then handle IIIF URLs and manifests
    manuscripts_with_iiif = filtered_manuscripts.exclude(
        Q(iiif_url__isnull=True) | Q(iiif_url="")
    ).values_list("siglum", "iiif_url")

    iiif_urls = dict(manuscripts_with_iiif)
    iiif_manifest = {
        siglum: get_manifest_data(url) for siglum, url in manuscripts_with_iiif
    }

    # Process line codes
    line_codes = []
    for line_code in filtered_linecodes:
        folio = line_code.associated_folio
        if folio:
            line_codes.append(
                {
                    "line_code": line_code.code,
                    "manuscript": (
                        folio.manuscript.siglum if folio.manuscript else "N/A"
                    ),
                    "folio": folio.folio_number,
                }
            )
        else:
            line_codes.append(
                {
                    "line_code": line_code.code,
                    "manuscript": "No manuscript assigned.",
                    "folio": "No folio assigned.",
                }
            )

    context = {
        "toponym": filtered_toponym,
        "manuscripts": filtered_manuscripts,
        "aggregated_aliases": aggregated_aliases,
        "folios": filtered_folios,
        "iiif_manifest": iiif_manifest,
        "iiif_urls": iiif_urls,
        "line_codes": line_codes,
    }

    return render(request, "gazetteer/gazetteer_single.html", context)


def search_toponyms(request):
    query = request.GET.get("q", "")
    try:
        if query:
            alias_results = LocationAlias.objects.filter(
                Q(placename_modern__icontains=query)
                | Q(placename_ancient__icontains=query)
                | Q(placename_from_mss__icontains=query)
                | Q(
                    location__name__icontains=query
                )  # Follow the relationship to Location's name field
            ).distinct()
        else:
            alias_results = LocationAlias.objects.all()
        return render(
            request, "gazetteer/gazetteer_results.html", {"aliases": alias_results}
        )
    except Exception as e:
        logger.error("Error in search_toponyms: %s", e)
        return JsonResponse({"error": str(e)}, status=500)


class ToponymViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ToponymSerializer

    def get_queryset(self):
        """
        Optionally filters the queryset based on the 'q' query parameter
        and returns all objects if no specific filter is applied.
        """
        queryset = Location.objects.all()
        query = self.request.query_params.get("q", None)
        if query is not None:
            queryset = queryset.filter(country__icontains=query)
        return queryset


class SingleManuscriptViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SingleManuscriptSerializer
    lookup_field = "siglum"

    def get_queryset(self):
        """
        Optionally filters the queryset based on the 'q' query parameter
        and returns all objects if no specific filter is applied.
        """
        queryset = SingleManuscript.objects.all()
        query = self.request.query_params.get("q", None)
        if query is not None:
            queryset = queryset.filter(siglum__icontains=query)
        return queryset
