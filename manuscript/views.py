from html import unescape

from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from manuscript.models import SingleManuscript, Stanza


def index(request: HttpRequest):
    return render(request, "index.html")


def about(request: HttpRequest):
    return render(request, "about.html")


def stanzas(request: HttpRequest):
    stanzas = Stanza.objects.all().order_by("stanza_line_code_starts")
    for stanza in stanzas:
        stanza.stanza_text = unescape(stanza.stanza_text)
    return render(request, "stanzas.html", {"stanzas": stanzas})


def manuscripts(request: HttpRequest):
    manuscripts = SingleManuscript.objects.all()
    return render(request, "manuscripts.html", {"manuscripts": manuscripts})
