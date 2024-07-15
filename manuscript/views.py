from collections import defaultdict
from html import unescape

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from rest_framework import viewsets

from manuscript.models import Location, SingleManuscript, Stanza, StanzaTranslated
from manuscript.serializers import ToponymSerializer


def process_stanzas(stanzas, is_translated=False):
    books = defaultdict(lambda: defaultdict(list))
    for stanza in stanzas:
        book_number = int(stanza.stanza_line_code_starts.split(".")[0])
        stanza_number = int(stanza.stanza_line_code_starts.split(".")[1])

        if is_translated:
            stanza.unescaped_stanza_text = unescape(stanza.stanza_translation)
        else:
            stanza.unescaped_stanza_text = unescape(stanza.stanza_text)

        books[book_number][stanza_number].append(stanza)

    return {k: dict(v) for k, v in books.items()}


def index(request: HttpRequest):
    return render(request, "index.html")


def about(request: HttpRequest):
    return render(request, "about.html")


def stanzas(request: HttpRequest):
    stanzas = Stanza.objects.all().order_by("stanza_line_code_starts")
    translated_stanzas = StanzaTranslated.objects.all().order_by(
        "stanza_line_code_starts"
    )
    manuscripts = SingleManuscript.objects.all()
    default_manuscript = SingleManuscript.objects.get(siglum="TEST")

    books = process_stanzas(stanzas)
    translated_books = process_stanzas(translated_stanzas)

    books = {k: dict(v) for k, v in books.items()}
    translated_books = {k: dict(v) for k, v in translated_books.items()}

    return render(
        request,
        "stanzas.html",
        {
            "stanzas": stanzas,
            "translated": translated_stanzas,
            "books": books,
            "translated_books": translated_books,
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
    toponym_objs = Location.objects.all()
    return render(request, "gazetteer/gazetteer_index.html", {"toponyms": toponym_objs})


def toponym(request: HttpRequest, toponym_param: int):
    filtered_toponym = get_object_or_404(Location, toponym=toponym_param)
    filtered_manuscript = get_object_or_404(
        SingleManuscript, folio__locations_mentioned__toponym=toponym_param
    )
    return render(
        request,
        "toponym_single.html",
        {"toponym": filtered_toponym, "manuscript": filtered_manuscript},
    )


def search_toponyms(request):
    query = request.GET.get("q", "")
    if query:
        toponym_results = Location.objects.filter(country__icontains=query)
    else:
        toponym_results = Location.objects.all()
    return render(
        request, "gazetteer/gazetteer_results.html", {"toponyms": toponym_results}
    )


class ToponymViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Location.objects.all()
    serializer_class = ToponymSerializer
