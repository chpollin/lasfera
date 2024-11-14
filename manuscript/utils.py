import json
from datetime import timedelta
from functools import lru_cache

import requests
from django.core.cache import cache


@lru_cache(maxsize=1)
def get_manifest():
    """
    Fetch the IIIF manifest with in-memory caching
    The lru_cache will keep the manifest in memory for the lifetime of the process
    """
    manifest_url = "https://digi.vatlib.it/iiif/MSS_Urb.lat.752/manifest.json"
    response = requests.get(manifest_url)
    return response.json()


def get_canvas_id_for_folio(folio_number):
    """Look up the canvas ID for a given folio number (e.g., "1r")"""
    try:
        manifest = get_manifest()
        for canvas in manifest["sequences"][0]["canvases"]:
            if canvas["label"] == folio_number:
                return canvas["@id"]
        return None
    except Exception as e:
        print(f"Error fetching canvas ID for folio {folio_number}: {e}")
        return None
