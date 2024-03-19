from django.conf import settings
from django.db import models


class Library(models.Model):
    city = models.CharField(max_length=255, blank=True, null=True)
    library = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.library + ", " + self.city

    class Meta:
        verbose_name_plural = "Libraries"


class ManuscriptLocation(models.Model):
    id = models.AutoField(primary_key=True)
    library = models.ForeignKey(
        Library, on_delete=models.CASCADE, blank=True, null=True
    )
    shelfmark = models.CharField(max_length=255, blank=True, null=True)
    digitized_url = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        help_text="The URL to the digitized manuscript. If there isn't one, leave blank.",
    )

    def __str__(self):
        return (
            self.library.library
            + ", "
            + self.library.city
            + " ("
            + self.shelfmark
            + ")"
        )

    class Meta:
        verbose_name = "Manuscript Location"


class EditorialStatus(models.Model):
    id = models.AutoField(primary_key=True)
    manuscript = models.ForeignKey(
        "SingleManuscript", on_delete=models.PROTECT, blank=True, null=True
    )
    siglum = models.CharField(max_length=255, blank=True, null=True)
    editorial_priority = models.IntegerField(blank=True, null=True)
    collated = models.BooleanField(blank=True, null=True)
    access = models.IntegerField(blank=True, null=True)
    digitized = models.BooleanField(blank=True, null=True)
    spatial_priority = models.CharField(max_length=6, blank=True, null=True)
    dataset = models.CharField(max_length=255, blank=True, null=True)
    group = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Editorial Status"
        verbose_name_plural = "Editorial Status"


class Reference(models.Model):
    id = models.AutoField(primary_key=True)
    manuscript = models.ForeignKey(
        "SingleManuscript", on_delete=models.PROTECT, blank=True, null=True
    )
    bert = models.CharField(max_length=6, blank=True, null=True)
    reference = models.CharField(max_length=255, blank=True, null=True)


class Codex(models.Model):
    id = models.AutoField(primary_key=True)
    support = models.CharField(max_length=255, blank=True, null=True)
    height = models.IntegerField(blank=True, null=True, help_text="in cm")
    date = models.CharField(max_length=255, blank=True, null=True)
    folia = models.CharField(max_length=255, blank=True, null=True)
    lines_per_page = models.CharField(max_length=255, blank=True, null=True)
    related_manuscript = models.ForeignKey(
        "SingleManuscript", on_delete=models.PROTECT, blank=True, null=True
    )

    class Meta:
        verbose_name_plural = "Codex"


class TextDecoration(models.Model):
    id = models.AutoField(primary_key=True)
    manuscript = models.ForeignKey(
        "SingleManuscript", on_delete=models.PROTECT, blank=True, null=True
    )
    text_script = models.CharField(max_length=255, blank=True, null=True)
    label_script = models.CharField(max_length=255, blank=True, null=True)
    diagrams = models.BooleanField(blank=True, null=True)
    maps = models.BooleanField(blank=True, null=True)
    illumination = models.BooleanField(blank=True, null=True)
    other = models.CharField(max_length=255, blank=True, null=True)
    relative_quality = models.CharField(max_length=255, blank=True, null=True)


class Detail(models.Model):
    id = models.AutoField(primary_key=True)
    manuscript = models.ForeignKey(
        "SingleManuscript", on_delete=models.PROTECT, blank=True, null=True
    )
    author_attribution = models.CharField(max_length=255, blank=True, null=True)
    scribe_attribution = models.CharField(max_length=255, blank=True, null=True)
    book_headings = models.BooleanField(blank=True, null=True)
    book_headings_notes = models.CharField(max_length=255, blank=True, null=True)
    book_initials = models.BooleanField(blank=True, null=True)
    book_initials_notes = models.CharField(max_length=255, blank=True, null=True)
    stanza_headings = models.BooleanField(blank=True, null=True)
    stanza_headings_notes = models.CharField(max_length=255, blank=True, null=True)
    stanza_initials = models.BooleanField(blank=True, null=True)
    stanza_initials_notes = models.CharField(max_length=255, blank=True, null=True)
    marginal_rubrics = models.BooleanField(blank=True, null=True)
    marginal_rubrics_notes = models.CharField(max_length=255, blank=True, null=True)
    filigree = models.BooleanField(blank=True, null=True)
    filigree_notes = models.CharField(max_length=255, blank=True, null=True)
    abbreviations = models.BooleanField(blank=True, null=True)
    abbreviations_notes = models.CharField(max_length=255, blank=True, null=True)
    catchwords = models.BooleanField(blank=True, null=True)
    catchwords_notes = models.CharField(max_length=255, blank=True, null=True)
    mabel_label = models.CharField(max_length=255, blank=True, null=True)
    map_labels = models.BooleanField(blank=True, null=True)
    map_labels_notes = models.CharField(max_length=255, blank=True, null=True)
    distance_lines = models.BooleanField(blank=True, null=True)
    distance_numbers = models.BooleanField(blank=True, null=True)
    distance_numbers_notes = models.CharField(max_length=255, blank=True, null=True)
    coat_of_arms = models.BooleanField(blank=True, null=True)
    coat_of_arms_notes = models.CharField(max_length=255, blank=True, null=True)

    is_sea_red = models.BooleanField(blank=True, null=True)
    laiazzo = models.BooleanField(blank=True, null=True)
    tabriz = models.BooleanField(blank=True, null=True)
    rhodes_status = models.CharField(max_length=255, blank=True, null=True)


class ViewerNote(models.Model):
    id = models.AutoField(primary_key=True)
    date_seen = models.DateField(blank=True, null=True)
    # the viewer is a dropdown from available users in the system
    viewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="viewer",
        help_text="The user who viewed the manuscript.",
    )

    notes = models.TextField(blank=True, null=True)
    related_manuscript = models.ForeignKey(
        "SingleManuscript", on_delete=models.PROTECT, blank=True, null=True
    )


class Stanza(models.Model):
    STANZA_LANGUAGE = (
        ("en", "English"),
        ("it", "Italian"),
        ("la", "Latin"),
        ("fr", "French"),
    )

    id = models.AutoField(primary_key=True)
    related_folio = models.ForeignKey(
        "Folio",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    stanza_line_number_on_page = models.IntegerField(
        blank=True,
        null=True,
        help_text="The line number of the stanza on the folio in the manuscript.",
    )
    stanza_number = models.IntegerField(
        blank=True,
        null=True,
        help_text="The number of the stanza in the manuscript.",
    )
    stanza_text = models.TextField(blank=True, null=True)
    stanza_notes = models.TextField(blank=True, null=True)
    stanza_translation = models.TextField(blank=True, null=True)
    stanza_language = models.CharField(
        max_length=2, choices=STANZA_LANGUAGE, blank=True, null=True
    )
    stanza_translation_notes = models.TextField(blank=True, null=True)
    manuscript = models.ForeignKey(
        "SingleManuscript", on_delete=models.PROTECT, blank=True, null=True
    )
    locations_mentioned = models.ManyToManyField(
        "Location",
        blank=True,
        help_text="Locations mentioned in the stanza.",
    )


class Folio(models.Model):
    """This provides a way to collect several stanzas onto a single page,
    and associate them with a single manuscript."""

    id = models.AutoField(primary_key=True)
    folio_number = models.IntegerField(blank=True, null=True)
    folio_notes = models.TextField(blank=True, null=True)
    manuscript = models.ForeignKey(
        "SingleManuscript", on_delete=models.PROTECT, blank=True, null=True
    )
    image = models.ImageField(
        null=True,
        blank=True,
        help_text="The image of the page from the manuscript.",
    )
    iiif_url = models.URLField(
        blank=True,
        null=True,
        help_text="Provide a IIIF manifest to a page in the manuscript. If there isn't one, leave blank.",
        verbose_name="IIIF URL",
    )


class SingleManuscript(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    library = models.ForeignKey(
        ManuscriptLocation, on_delete=models.CASCADE, blank=True, null=True
    )
    iiif_url = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        help_text="The URL to the IIIF manifest for the manuscript. If there isn't one, leave blank.",
        verbose_name="IIIF URL",
    )
    gazetteer_url = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        help_text="The URL to an external gazetteer for the manuscript. If there isn't one, leave blank.",
        verbose_name="Gazetteer URL",
    )
    # Think about how we might manage multiple authority files
    authority_file = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        help_text="The URL to the authority file for the manuscript. If there isn't one, leave blank.",
        verbose_name="Authority File",
    )
    purl_url = models.URLField(
        blank=True,
        null=True,
        help_text="The URL to the permanent URL for the manuscript. If there isn't one, leave blank.",
        verbose_name="Permanent URL",
    )

    provenance = models.TextField(blank=True, null=True)
    manuscript_lost = models.BooleanField(blank=True, null=True, default=False)
    manuscript_destroyed = models.BooleanField(blank=True, null=True, default=False)

    class Meta:
        verbose_name = "Manuscript"


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    authority_file = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        help_text="The URL to the authority file for the location. If there isn't one, leave blank.",
    )

    def __str__(self):
        return self.city + ", " + self.country
