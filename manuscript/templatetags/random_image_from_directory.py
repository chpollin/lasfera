import os
import random

from django import template
from django.conf import settings

register = template.Library()


@register.filter
def random_image_from_directory(directory):
    static_dir = None

    # Check if STATIC_ROOT exists and use it in production
    if os.path.exists(settings.STATIC_ROOT):
        static_dir = os.path.join(settings.STATIC_ROOT, directory)
        if not os.path.exists(static_dir):
            static_dir = None

    # Fallback to STATICFILES_DIRS in development
    if static_dir is None:
        for static_dir_path in settings.STATICFILES_DIRS:
            potential_dir = os.path.join(static_dir_path, directory)
            if os.path.exists(potential_dir):
                static_dir = potential_dir
                break

    if static_dir is None:
        # Optionally log this instead of printing in production
        print("Directory does not exist")
        return ""

    images = [
        f for f in os.listdir(static_dir) if os.path.isfile(os.path.join(static_dir, f))
    ]
    if not images:
        # Optionally log this instead of printing in production
        print("No images found")
        return ""

    random_image = random.choice(images)
    image_url = os.path.join(settings.STATIC_URL, directory, random_image)
    return image_url
