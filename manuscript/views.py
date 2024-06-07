from collections import defaultdict
from html import unescape

from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from manuscript.models import SingleManuscript, Stanza


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
    manuscripts = SingleManuscript.objects.all()
    return render(request, "manuscripts.html", {"manuscripts": manuscripts})


def manuscript(request: HttpRequest, siglum: str):
    manuscript = get_object_or_404(SingleManuscript, siglum=siglum)
    folios = manuscript.folio_set.prefetch_related("locations_mentioned").all()
    return render(
        request,
        "manuscript_single.html",
        {
            "manuscript": manuscript,
            "folios": folios,
            "iiif_manifest": manuscript.iiif_url,
        },
    )
