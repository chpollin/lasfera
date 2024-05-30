from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from manuscript.models import Stanza


def index(request: HttpRequest):
    stanzas = Stanza.objects.all().order_by("stanza_line_code_starts")
    return render(request, "index.html", {"stanzas": stanzas})
