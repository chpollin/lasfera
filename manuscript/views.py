from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.views import generic


def index(request: HttpRequest):
    return render(request, "index.html", {})
