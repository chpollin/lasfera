import logging
import os
import random
import re
from collections import defaultdict
from html import unescape

from django.conf import settings
from django.db.models import Q
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets

from manuscript.models import (
    Location,
    LocationAlias,
    SingleManuscript,
    Stanza,
    StanzaTranslated,
)
from manuscript.serializers import SingleManuscriptSerializer, ToponymSerializer
from pages.models import AboutPage, SitePage

logger = logging.getLogger(__name__)


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
        "is_index": True,
        "image_urls": image_urls,
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


def stanzas(request: HttpRequest):
    stanzas = Stanza.objects.all().order_by("stanza_line_code_starts")
    translated_stanzas = StanzaTranslated.objects.all().order_by(
        "stanza_line_code_starts"
    )
    manuscripts = SingleManuscript.objects.all()
    default_manuscript = SingleManuscript.objects.get(siglum="TEST")

    books = process_stanzas(stanzas)
    translated_books = process_stanzas(translated_stanzas)

    paired_books = {}
    for book_number, stanza_dict in books.items():
        paired_books[book_number] = []
        for stanza_number, original_stanzas in stanza_dict.items():
            translated_stanza_group = translated_books.get(book_number, {}).get(
                stanza_number, []
            )
            paired_books[book_number].append(
                {
                    "original": original_stanzas,
                    "translated": translated_stanza_group,
                }
            )

    return render(
        request,
        "stanzas.html",
        {
            "paired_books": paired_books,
            "manuscripts": manuscripts,
            "default_manuscript": default_manuscript,
        },
    )


def manuscripts(request: HttpRequest):
    manuscript_objs = SingleManuscript.objects.all()
    return render(request, "manuscripts.html", {"manuscripts": manuscript_objs})


def manuscript(request: HttpRequest, siglum: str):
    get_manuscript = get_object_or_404(SingleManuscript, siglum=siglum)
    folios = get_manuscript.folio_set.prefetch_related("locations_mentioned").all()

    # Fetch related LocationAlias objects for each location mentioned in the folios
    for folio in folios:
        for location in folio.locations_mentioned.all():
            alias = (
                LocationAlias.objects.filter(location=location)
                .values("placename_modern", "placename_from_mss")
                .first()
            )
            location.alias = alias

    return render(
        request,
        "manuscript_single.html",
        {
            "manuscript": get_manuscript,
            "folios": folios,
            "iiif_manifest": get_manuscript.iiif_url,
        },
    )


def toponyms(request: HttpRequest):
    # Get unique and sorted LocationAlias objects based on placename_modern
    toponym_alias_objs = (
        LocationAlias.objects.values("placename_modern", "location_id")
        .distinct()
        .order_by("placename_modern")
    )
    return render(
        request, "gazetteer/gazetteer_index.html", {"aliases": toponym_alias_objs}
    )


def toponym(request: HttpRequest, toponym_param: int):
    # The following variables filter the data based on the toponym_param
    filtered_toponym = get_object_or_404(Location, pk=toponym_param)
    filtered_manuscripts = SingleManuscript.objects.filter(
        folio__locations_mentioned=toponym_param
    ).distinct()
    filtered_folios = filtered_toponym.folio_set.all()
    filtered_linecodes = filtered_toponym.linecode_set.all()

    # Process the aliases
    processed_aliases = []
    aggregated_aliases = {
        "placename_aliases": [],
        "placename_moderns": [],
        "placename_standardizeds": [],
        "placename_from_msss": [],
        "placename_ancients": [],
    }
    for alias in filtered_toponym.locationalias_set.all():
        placename_alias = (
            [name.strip() for name in alias.placename_alias.split(",")]
            if alias.placename_alias
            else []
        )
        placename_modern = (
            [name.strip() for name in alias.placename_modern.split(",")]
            if alias.placename_modern
            else []
        )
        placename_standardized = (
            [name.strip() for name in alias.placename_standardized.split(",")]
            if alias.placename_standardized
            else []
        )
        placename_from_mss = (
            [name.strip() for name in alias.placename_from_mss.split(",")]
            if alias.placename_from_mss
            else []
        )
        placename_ancient = (
            [name.strip() for name in alias.placename_ancient.split(",")]
            if alias.placename_ancient
            else []
        )

        processed_aliases.append(
            {
                "placename_alias": placename_alias,
                "placename_modern": placename_modern,
                "placename_standardized": placename_standardized,
                "placename_from_mss": placename_from_mss,
                "placename_ancient": placename_ancient,
            }
        )

        # Aggregate the aliases
        aggregated_aliases["placename_aliases"].extend(placename_alias)
        aggregated_aliases["placename_moderns"].extend(placename_modern)
        aggregated_aliases["placename_standardizeds"].extend(placename_standardized)
        aggregated_aliases["placename_from_msss"].extend(placename_from_mss)
        aggregated_aliases["placename_ancients"].extend(placename_ancient)

        processed_aliases.append(
            {
                "placename_alias": placename_alias,
                "placename_modern": placename_modern,
                "placename_standardized": placename_standardized,
                "placename_from_mss": placename_from_mss,
                "placename_ancient": placename_ancient,
            }
        )

    # Get associated iiif_url fields from SingleManuscript
    for manuscript in filtered_manuscripts:
        manuscript.iiif_url = manuscript.iiif_url

    # Get associated iiif_url from the Folio
    iiif_urls = []
    for line_code in filtered_linecodes:
        if line_code.associated_iiif_url:
            folio = line_code.associated_folio
            if folio:
                manuscript = folio.manuscript
                iiif_urls.append(
                    {
                        "iiif_url": line_code.associated_iiif_url,
                        "manuscript": manuscript.siglum,
                    }
                )

    # The line codes should indicate which folio and manuscript they belong to.
    line_codes = []
    for line_code in filtered_linecodes:
        # Retrieve the Folio object through the associated_folio field
        folio = line_code.associated_folio
        # we create a variable that strips out the characters from the folio number so we're left
        # with just the number
        folio_number = re.sub(r"\D", "", folio.folio_number) if folio else None
        if folio:
            # Retrieve the Manuscript object through the Folio model
            manuscript = folio.manuscript
            line_codes.append(
                {
                    "line_code": line_code.code,
                    "manuscript": manuscript.siglum,
                    "folio": folio.folio_number,
                    "folio_number": folio_number,
                }
            )

    return render(
        request,
        "gazetteer/gazetteer_single.html",
        {
            "toponym": filtered_toponym,
            "manuscripts": filtered_manuscripts,
            "aliases": processed_aliases,
            "aggregated_aliases": aggregated_aliases,
            "folios": filtered_folios,
            "iiif_manifest": filtered_manuscripts[0].iiif_url,
            "iiif_urls": iiif_urls,
            "line_codes": line_codes,
        },
    )


def search_toponyms(request):
    query = request.GET.get("q", "")
    try:
        if query:
            alias_results = LocationAlias.objects.filter(
                Q(placename_modern__icontains=query)
                | Q(placename_ancient__icontains=query)
                | Q(placename_from_mss__icontains=query)
            ).distinct()
            logger.info("Toponym search query: %s", query)
            logger.info("Toponym search results: %s", alias_results.query)
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
