import logging
import re

from bs4 import BeautifulSoup
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django_prose_editor.fields import ProseEditorField
from prose.fields import RichTextField

logger = logging.getLogger(__name__)


def validate_line_number_code(value):
    pattern = r"^\d{2}\.\d{2}\.\d{2}(-\d{2}\.\d{2}\.\d{2})?$"
    if not re.match(pattern, value):
        raise ValidationError(
            'Invalid number format. Expected format: "01.01.04" or "01.01.04-01.01.16"'
        )


def validate_line_number_variant_code(value):
    # expected: 01.01.04a or 04.05.01b etc.
    pattern = r"^\d{2}\.\d{2}\.\d{2}[a-z]$"
    if not re.match(pattern, value):
        raise ValidationError('Invalid number format. Expected format: "01.01.04a"')


class Library(models.Model):
    """Library or collection that holds a manuscript"""

    city = models.CharField(max_length=255, blank=True, null=True)
    library = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Libraries"
        unique_together = ["city", "library"]
        ordering = ["city", "library"]

    def __str__(self) -> str:
        city = self.city if self.city is not None else "No city name provided"
        library = self.library if self.library is not None else ""
        return city + " - " + library

    def natural_key(self):
        return (self.library, self.city)


class EditorialStatus(models.Model):
    """The editorial status of a manuscript"""

    id = models.AutoField(primary_key=True)
    manuscript = models.ForeignKey(
        "SingleManuscript", on_delete=models.CASCADE, blank=True, null=True
    )
    # siglum = models.CharField(max_length=255, blank=True, null=True, unique=True)
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

    class Meta:
        verbose_name = "Editorial Status"
        verbose_name_plural = "Editorial Status"

    def __str__(self) -> str:
        if self.editorial_priority is not None:
            return "Editorial Priority: " + str(self.editorial_priority)
        return "Editorial Status"


class Reference(models.Model):
    """References within the manuscript"""

    id = models.AutoField(primary_key=True)
    manuscript = models.ForeignKey(
        "SingleManuscript", on_delete=models.CASCADE, blank=True, null=True
    )
    bert = models.CharField(max_length=6, blank=True, null=True)
    reference = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        if self.reference is not None:
            return self.reference
        return "Reference"


class Codex(models.Model):
    """Information and details about the manuscript"""

    id = models.AutoField(primary_key=True)
    support = models.CharField(max_length=255, blank=True, null=True)
    height = models.IntegerField(blank=True, null=True, help_text="in cm")
    date = models.CharField(max_length=255, blank=True, null=True)
    folia = models.CharField(max_length=255, blank=True, null=True)
    lines_per_page = models.CharField(max_length=255, blank=True, null=True)
    related_manuscript = models.ForeignKey(
        "SingleManuscript", on_delete=models.CASCADE, blank=True, null=True
    )

    class Meta:
        verbose_name_plural = "Codex"

    def __str__(self) -> str:
        if self.id is not None:
            return str(self.id)
        return str(self.id)


class TextDecoration(models.Model):
    """Details and information about the text of the manuscript"""

    id = models.AutoField(primary_key=True)
    manuscript = models.ForeignKey(
        "SingleManuscript", on_delete=models.CASCADE, blank=True, null=True
    )
    text_script = models.CharField(max_length=255, blank=True, null=True)
    label_script = models.CharField(max_length=255, blank=True, null=True)
    diagrams = models.CharField(blank=True, null=True)
    maps = models.CharField(blank=True, null=True)
    illumination = models.CharField(blank=True, null=True)
    white_vine_work = models.CharField(blank=True, null=True)
    other = models.CharField(max_length=255, blank=True, null=True)
    relative_quality = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        if self.text_script is not None:
            return self.text_script
        else:
            return "Text Decoration"


class Detail(models.Model):
    """Details about the manuscript including author, scribe, headings, etc."""

    STANZA_RUBRIC_CHOICES = (
        ("sh", "Stanza Headings"),
        ("mr", "Marginal Rubrics"),
        ("ne", "Neither"),
        ("uk", "Unknown"),
    )

    id = models.AutoField(primary_key=True)
    manuscript = models.ForeignKey(
        "SingleManuscript", on_delete=models.CASCADE, blank=True, null=True
    )
    author_attribution = models.CharField(max_length=510, blank=True, null=True)
    scribe_attribution = models.CharField(max_length=510, blank=True, null=True)
    book_headings = RichTextField(blank=True, null=True)
    book_initials = RichTextField(blank=True, null=True)
    stanza_headings_marginal_rubrics = models.CharField(
        max_length=2, choices=STANZA_RUBRIC_CHOICES, blank=True, null=True
    )
    stanza_headings_marginal_rubrics_notes = RichTextField(
        max_length=510, blank=True, null=True
    )
    stanza_initials = RichTextField(max_length=510, blank=True, null=True)
    stanzas_separated = models.CharField(blank=True, null=True)
    stanzas_ed = models.CharField(blank=True, null=True)
    filigree = models.CharField(
        max_length=510,
        blank=True,
        null=True,
        verbose_name="Flourished/Filigree Initials",
    )
    standard_water = models.CharField(blank=True, null=True)
    abbreviations = RichTextField(max_length=510, blank=True, null=True)
    catchwords = RichTextField(max_length=510, blank=True, null=True)
    mabel_label = models.CharField(max_length=510, blank=True, null=True)
    map_labels = RichTextField(max_length=510, blank=True, null=True)
    distance_lines = models.CharField(blank=True, null=True)
    distance_numbers = models.CharField(max_length=510, blank=True, null=True)
    coat_of_arms = models.CharField(max_length=510, blank=True, null=True)

    is_sea_red = models.CharField(
        blank=True, null=True, verbose_name="Is the Red Sea colored red?"
    )
    laiazzo = models.CharField(blank=True, null=True)
    tabriz = models.CharField(blank=True, null=True)
    rhodes_status = models.CharField(max_length=510, blank=True, null=True)

    def __str__(self) -> str:
        if self.id is not None:
            return str(self.id)
        else:
            return "Detail"


class ViewerNote(models.Model):
    """Notes on the manuscript from a particular user"""

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

    def __str__(self) -> str:
        if self.viewer is not None:
            return self.viewer
        return "Viewer Note"


class StanzaVariant(models.Model):
    """Notes about variants in a stanza"""

    LINE_VARIANTS = (
        ("lf", "Lines Flipped"),
        ("dw", "Different Words"),
        ("do", "Different Order"),
        ("dp", "Different Punctuation"),
        ("ds", "Different Spelling"),
        ("dc", "Different Capitalization"),
    )

    # TODO: Ability to have variation in lines
    id = models.AutoField(primary_key=True)
    stanza_variation = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Significant Variations",
        help_text="The variation in the stanza.",
    )
    stanza_variation_line_code_starts = models.CharField(
        blank=True,
        null=True,
        validators=[validate_line_number_variant_code],
        max_length=20,
        help_text="Stanza variant line code in the form of '01.01.01a'.",
        verbose_name="Variant line code",
    )

    stanza = models.ForeignKey(
        "Stanza", on_delete=models.PROTECT, blank=True, null=True
    )

    def provide_snippet_of_stanza(self):
        return self.stanza.stanza_text[:100]

    def __str__(self) -> str:
        soup = BeautifulSoup(self.stanza_variation, "html.parser")
        text = soup.get_text()

        return text[:100] + "..."


class Stanza(models.Model):
    """A stanza from the manuscript."""

    STANZA_LANGUAGE = (
        ("en", "English"),
        ("it", "Italian"),
        ("la", "Latin"),
        ("fr", "French"),
    )

    id = models.AutoField(primary_key=True)
    related_manuscript = models.ForeignKey(
        "SingleManuscript",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        help_text="Required. The manuscript to which the stanza belongs.",
    )
    related_folio = models.ForeignKey(
        "Folio",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="Optional. The folio to which the stanza belongs.",
    )
    stanza_line_code_starts = models.CharField(
        blank=True,
        null=True,
        validators=[validate_line_number_code],
        max_length=20,
        help_text="Indicate where the folio begins. Input the text by book, stanza, and line number. For example: 01.01.01 refers to book 1, stanza 1, line 1.",
    )
    stanza_line_code_ends = models.CharField(
        blank=True,
        null=True,
        validators=[validate_line_number_code],
        max_length=20,
        help_text="Indicate where the folio ends. Input the text by book, stanza, and line number. For example: 01.01.07 refers to book 1, stanza 1, line 7.",
    )
    stanza_text = RichTextField(blank=True, null=True)
    stanza_notes = RichTextField(blank=True, null=True)

    def __str__(self) -> str:
        if self.stanza_line_code_starts is not None:
            return self.stanza_line_code_starts
        elif self.stanza_line_code_ends is not None:
            return self.stanza_line_code_starts + " - " + self.stanza_line_code_ends
        elif self.stanza_line_variation is not None:
            return (
                self.stanza_line_code_starts
                + " - "
                + self.stanza_line_code_ends
                + " - "
                + self.stanza_line_variation
            )
        else:
            return ""

    def get_book(self):
        return int(self.stanza_line_code.split(".")[0])

    def get_stanza(self):
        return int(self.stanza_line_code.split(".")[1])

    def get_line(self):
        return int(
            self.your_field.split(".")[2].split("-")[0]
        )  # Handle the case of a range

    def derive_folio_location(self):
        # We derive the folio based on the line code.
        if self.stanza_line_code_starts is not None:
            line_code = self.stanza_line_code_starts
        elif self.stanza_line_code_ends is not None:
            line_code = self.stanza_line_code_ends
        else:
            return None

        book, stanza, line = line_code.split(".")
        return Folio.objects.filter(
            manuscript=self.related_folio.manuscript, folio_number=book
        ).first()

    class Meta:
        ordering = ["id"]


class Folio(models.Model):
    """This provides a way to collect several stanzas onto a single page, and associate them with a single manuscript."""

    FOLIO_MAP_CHOICES = (
        ("yes", "Yes"),
        ("yes_toponyms", "Yes with toponyms"),
        ("yes_no_toponyms", "Yes without toponyms"),
        ("no", "No"),
    )

    id = models.AutoField(primary_key=True)
    folio_number = models.CharField(blank=True, null=True)
    folio_notes = RichTextField(blank=True, null=True)
    manuscript = models.ForeignKey(
        "SingleManuscript", on_delete=models.CASCADE, blank=True, null=True
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
    folio_includes_map = models.CharField(
        blank=True,
        null=True,
        choices=FOLIO_MAP_CHOICES,
        verbose_name="Does the folio include a map?",
    )
    locations_mentioned = models.ManyToManyField(
        "Location",
        blank=True,
        help_text="Toponyms associated with the folio.",
        verbose_name="Associated toponyms",
    )

    def __str__(self) -> str:
        if self.folio_number is not None:
            return f"Folio {self.folio_number}, from manuscript {self.manuscript}"
        return f"Folio has no folio number but is associated with manuscript {self.manuscript}"

    class Meta:
        ordering = ["folio_number"]


class SingleManuscript(models.Model):
    """A representation of a single manuscript"""

    id = models.AutoField(primary_key=True)
    item_id = models.IntegerField(blank=False, null=False, unique=True)
    siglum = models.CharField(max_length=20, blank=True, null=True, unique=True)
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
    purl_url = models.URLField(
        blank=True,
        null=True,
        help_text="The URL to the permanent URL for the manuscript. If there isn't one, leave blank.",
        verbose_name="Permanent URL",
    )
    digitized_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="The URL to the digitized manuscript. If there isn't one, leave blank.",
        verbose_name="Digitized URL",
    )

    provenance = RichTextField(blank=True, null=True)
    manuscript_lost = models.BooleanField(blank=True, null=True, default=False)
    manuscript_destroyed = models.BooleanField(blank=True, null=True, default=False)

    class Meta:
        verbose_name = "Manuscript"
        verbose_name_plural = "Manuscripts"
        ordering = ["siglum"]

    def __str__(self) -> str:
        if self.siglum:
            return self.siglum
        elif self.shelfmark:
            return self.shelfmark
        else:
            return "Manuscript"


class AuthorityFile(models.Model):
    """Include authority files for various aspects of a manuscript"""

    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="The name of the authority file",
    )
    authority_file_url = models.URLField(
        blank=True,
        null=True,
        help_text="The URL to the authority file for the manuscript.",
        verbose_name="Authority File URL",
    )
    manuscript = models.ForeignKey(
        "SingleManuscript", on_delete=models.PROTECT, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.authority_file_url}"

    class Meta:
        verbose_name = "Authority File"
        verbose_name_plural = "Authority Files"


class Location(models.Model):
    """Handle the location information and toponyms within a manuscript"""

    id = models.AutoField(primary_key=True)
    placename_id = models.CharField(blank=True, null=True, verbose_name="Placename ID")
    # TODO: this could be more than one... eg this toponym shows up at 2.3.4 and 1.4.7
    line_code = models.CharField(blank=True, null=True, help_text="Citation line code.")
    related_folio = models.ForeignKey(
        Folio, on_delete=models.CASCADE, blank=True, null=True
    )
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

    class Meta:
        verbose_name = "Toponym"
        verbose_name_plural = "Toponyms"
        ordering = ["country"]
        unique_together = ["country"]

    def __str__(self) -> str:
        if (
            self.pk is not None
        ):  # Only try to access locationalias_set if the Location has been saved
            return ", ".join(
                [
                    alias.placename_from_mss
                    for alias in self.locationalias_set.all()
                    if alias.placename_from_mss is not None
                ]
            )
        else:
            return super().__str__()

    def geocode(self):
        if self.latitude is None or self.longitude is None:
            try:
                from geopy.geocoders import Nominatim

                geolocator = Nominatim(user_agent="manuscript")
                location_alias = self.locationalias_set.first()
                if location_alias is not None:
                    location = geolocator.geocode(location_alias.placename_modern)
                    if location is not None:
                        self.latitude = str(location.latitude)
                        self.longitude = str(location.longitude)
                        self.save()
            except Exception as e:
                logger.warning(
                    "Warning in geocoding a toponym: %s %s", str(e), str(self)
                )


class LocationAlias(models.Model):
    """The alias of a location"""

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

    class Meta:
        verbose_name = "Location Alias"
        verbose_name_plural = "Location Aliases"
        ordering = ["placename_standardized"]
        unique_together = ["placename_standardized"]

    def __str__(self) -> str:
        return f"{self.placename_from_mss} / {self.placename_standardized} / {self.placename_modern} / {self.placename_alias}"
