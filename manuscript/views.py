from collections import defaultdict
from html import unescape

from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from manuscript.models import Location, SingleManuscript, Stanza


def index(request: HttpRequest):
    return render(request, "index.html")


def about(request: HttpRequest):
    return render(request, "about.html")


def stanzas(request: HttpRequest):
    stanzas = Stanza.objects.all().order_by("stanza_line_code_starts")

    books = defaultdict(lambda: defaultdict(list))
    for stanza in stanzas:
        book_number = int(stanza.stanza_line_code_starts.split(".")[0])
        stanza_number = int(stanza.stanza_line_code_starts.split(".")[1])

        stanza.unescaped_stanza_text = unescape(stanza.stanza_text)
        books[book_number][stanza_number].append(stanza)

    books = {k: dict(v) for k, v in books.items()}

    return render(request, "stanzas.html", {"stanzas": stanzas, "books": books})


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
    return render(request, "toponyms.html", {"toponyms": toponym_objs})


def toponym(request: HttpRequest, toponym_param: str):
    filtered_toponym = get_object_or_404(Location, toponym=toponym_param)
    filtered_manuscript = get_object_or_404(
        SingleManuscript, folio__locations_mentioned__toponym=toponym_param
    )
    return render(
        request,
        "toponym.html",
        {"toponym": filtered_toponym, "manuscript": filtered_manuscript},
    )
