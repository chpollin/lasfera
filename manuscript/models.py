import logging

from django.conf import settings
from django.db import models
from prose.fields import RichTextField

logger = logging.getLogger(__name__)


class Library(models.Model):
    city = models.CharField(max_length=255, blank=True, null=True)
    library = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.library + ", " + self.city

    class Meta:
        verbose_name_plural = "Libraries"


class EditorialStatus(models.Model):
    id = models.AutoField(primary_key=True)
    manuscript = models.ForeignKey(
        "SingleManuscript", on_delete=models.PROTECT, blank=True, null=True
    )
    siglum = models.CharField(max_length=255, blank=True, null=True)
    editorial_priority = models.IntegerField(blank=True, null=True)
    collated = models.CharField(blank=True, null=True)
    access = models.IntegerField(blank=True, null=True)
    spatial_priority = models.CharField(max_length=6, blank=True, null=True)
    dataset = models.CharField(max_length=255, blank=True, null=True)
    group = models.CharField(max_length=255, blank=True, null=True)
    iiif_url = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        help_text="The URL to the IIIF manifest for the manuscript. If there isn't one, leave blank.",
        verbose_name="IIIF URL",
    )

    def __str__(self):
        if self.siglum is not None:
            return self.siglum
        else:
            return "Editorial Status"

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

    def __str__(self):
        return self.reference


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

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "Codex"


class TextDecoration(models.Model):
    id = models.AutoField(primary_key=True)
    manuscript = models.ForeignKey(
        "SingleManuscript", on_delete=models.PROTECT, blank=True, null=True
    )
    text_script = models.CharField(max_length=255, blank=True, null=True)
    label_script = models.CharField(max_length=255, blank=True, null=True)
    diagrams = models.CharField(blank=True, null=True)
    maps = models.CharField(blank=True, null=True)
    illumination = models.CharField(blank=True, null=True)
    white_vine_work = models.CharField(blank=True, null=True)
    other = models.CharField(max_length=255, blank=True, null=True)
    relative_quality = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        if self.text_script is not None:
            return self.text_script
        else:
            return "Text Decoration"


class Detail(models.Model):
    # 1) stanza headings; 2) marginal rubrics; 3) neither; or 4) unknown.
    STANZA_RUBRIC_CHOICES = (
        ("sh", "Stanza Headings"),
        ("mr", "Marginal Rubrics"),
        ("ne", "Neither"),
        ("uk", "Unknown"),
    )

    id = models.AutoField(primary_key=True)
    manuscript = models.ForeignKey(
        "SingleManuscript", on_delete=models.PROTECT, blank=True, null=True
    )
    author_attribution = models.CharField(max_length=255, blank=True, null=True)
    scribe_attribution = models.CharField(max_length=255, blank=True, null=True)
    book_headings = models.BooleanField(blank=True, null=True)
    book_headings_notes = RichTextField(blank=True, null=True)
    book_initials = models.BooleanField(blank=True, null=True)
    book_initials_notes = RichTextField(blank=True, null=True)
    stanza_headings_marginal_rubrics = models.CharField(
        max_length=2, choices=STANZA_RUBRIC_CHOICES, blank=True, null=True
    )
    stanza_headings_marginal_rubrics_notes = RichTextField(
        max_length=255, blank=True, null=True
    )
    stanza_initials = models.BooleanField(blank=True, null=True)
    stanza_initials_notes = RichTextField(max_length=255, blank=True, null=True)
    filigree = models.BooleanField(blank=True, null=True)
    filigree_notes = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Flourished/Filigree Initials",
    )
    abbreviations = models.BooleanField(blank=True, null=True)
    abbreviations_notes = RichTextField(max_length=255, blank=True, null=True)
    catchwords = models.BooleanField(blank=True, null=True)
    catchwords_notes = RichTextField(max_length=255, blank=True, null=True)
    mabel_label = models.CharField(max_length=255, blank=True, null=True)
    map_labels = models.BooleanField(blank=True, null=True)
    map_labels_notes = RichTextField(max_length=255, blank=True, null=True)
    distance_lines = models.BooleanField(blank=True, null=True)
    distance_numbers = models.BooleanField(blank=True, null=True)
    distance_numbers_notes = RichTextField(max_length=255, blank=True, null=True)
    coat_of_arms = models.BooleanField(blank=True, null=True)
    coat_of_arms_notes = RichTextField(max_length=255, blank=True, null=True)

    is_sea_red = models.BooleanField(
        blank=True, null=True, verbose_name="Is the Red Sea colored red?"
    )
    laiazzo = models.BooleanField(blank=True, null=True)
    tabriz = models.BooleanField(blank=True, null=True)
    rhodes_status = models.CharField(max_length=255, blank=True, null=True)


class ViewerNote(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(blank=True, null=True)
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
    # manuscript = models.ForeignKey(
    #     "SingleManuscript", on_delete=models.PROTECT, blank=True, null=True
    # )
    locations_mentioned = models.ManyToManyField(
        "Location",
        blank=True,
        help_text="Locations mentioned in the stanza.",
        verbose_name="Associated toponyms",
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

    def __str__(self):
        return f"Folio page {self.folio_number} from manuscript: {self.manuscript}"


class SingleManuscript(models.Model):
    id = models.AutoField(primary_key=True)
    shelfmark = models.CharField(max_length=255, blank=True, null=True)
    library = models.ForeignKey(
        Library, on_delete=models.PROTECT, blank=True, null=True
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
    # TODO: Think about how we might manage multiple authority files
    authority_file_url = models.URLField(
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
    digitized_url = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        help_text="The URL to the digitized manuscript. If there isn't one, leave blank.",
        verbose_name="Digitized URL",
    )

    provenance = RichTextField(blank=True, null=True)
    manuscript_lost = models.BooleanField(blank=True, null=True, default=False)
    manuscript_destroyed = models.BooleanField(blank=True, null=True, default=False)

    def __str__(self) -> str:
        if self.shelfmark is not None:
            return (
                self.shelfmark
                + " ("
                + self.library.library
                + ", "
                + self.library.city
                + ")"
            )
        else:
            return "No shelfmark provided"

    class Meta:
        verbose_name = "Manuscript"
        verbose_name_plural = "Manuscripts"


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Modern country"
    )
    description = RichTextField(blank=True, null=True)
    latitude = models.FloatField(
        blank=True,
        null=True,
        help_text="Latitude in decimal degrees. If left blank, the system will attempt to geocode the location from the modern placename.",
    )
    longitude = models.FloatField(
        blank=True,
        null=True,
        help_text="Longitude in decimal degrees. If left blank, the system will attempt to geocode the location from the modern placename.",
    )
    authority_file = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        help_text="The URL to the authority file for the location. If there isn't one, leave blank.",
    )

    def __str__(self):
        aliases = ", ".join(
            [alias.placename_from_mss for alias in self.locationalias_set.all()]
        )
        return f"{self.country} ({aliases})"

    class Meta:
        verbose_name = "Toponym"
        verbose_name_plural = "Toponyms"
        ordering = ["country"]
        unique_together = ["country"]

    # On save, the following tries to derive the latlon from the town_city and country
    # fields. If successful, it stores the latlon in the latlon field.
    def save(self, *args, **kwargs):
        if self.latitude is None or self.longitude is None:
            try:
                from geopy.geocoders import Nominatim

                geolocator = Nominatim(user_agent="manuscript")
                location_alias = self.locationalias_set.first()
                if location_alias is not None:
                    location = geolocator.geocode(location_alias.placename_modern)

                    self.latitude = str(location.latitude)
                    self.longitude = str(location.longitude)
            except Exception as e:
                logger.warning("Warning in geocoding a toponym: " + str(e) + str(self))
        super().save(*args, **kwargs)


class LocationAlias(models.Model):
    id = models.AutoField(primary_key=True)
    placename_from_mss = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Transcribed placename",
        help_text="The placename as it appears in the manuscript.",
    )
    placename_standardized = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Standardized placename",
        help_text="The standardized name of the placename.",
    )
    placename_modern = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Modern placename",
        help_text="The modern name of the placename.",
    )
    placename_alias = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Additional aliases",
        help_text="Additional aliases for the placename.",
    )
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return f"{self.placename_from_mss} / {self.placename_standardized} / {self.placename_modern} / {self.placename_alias}"

    class Meta:
        verbose_name = "Location Alias"
        verbose_name_plural = "Location Aliases"
        ordering = ["placename_standardized"]
        unique_together = ["placename_standardized"]
