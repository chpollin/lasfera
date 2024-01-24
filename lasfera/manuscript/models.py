from django.db import models

class Library(models.Model):
    city = models.CharField(max_length=255, blank=True, null=True)
    library = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.library + ", " + self.city

class ManuscriptLocation(models.Model):
    id = models.AutoField(primary_key=True)
    library = models.ForeignKey(Library, on_delete=models.CASCADE, blank=True, null=True)
    shelfmark = models.CharField(max_length=255, blank=True, null=True)
    digitized_url = models.URLField(max_length=255, blank=True, null=True, help_text="The URL to the digitized manuscript. If there isn't one, leave blank.")

    def __str__(self):
        return self.library.library + ", " + self.library.city + " (" + self.shelfmark + ")"

class EditorialStatus(models.Model):
    id = models.AutoField(primary_key=True)
    manuscript = models.ForeignKey('SingleManuscript', on_delete=models.PROTECT, blank=True, null=True)
    siglum = models.CharField(max_length=255, blank=True, null=True)
    editorial_priority = models.IntegerField(blank=True, null=True)
    collated = models.BooleanField(blank=True, null=True)
    access = models.IntegerField(blank=True, null=True)
    digitized = models.BooleanField(blank=True, null=True)
    spatial_priority = models.CharField(max_length=6, blank=True, null=True)
    dataset = models.CharField(max_length=255, blank=True, null=True)
    group = models.CharField(max_length=255, blank=True, null=True)

class Reference(models.Model):
    id = models.AutoField(primary_key=True)
    bert = models.CharField(max_length=6, blank=True, null=True)
    reference = models.CharField(max_length=255, blank=True, null=True)

class Codex(models.Model):
    id = models.AutoField(primary_key=True)
    support = models.CharField(max_length=255, blank=True, null=True)
    height = models.IntegerField(blank=True, null=True, help_text="in cm")
    date = models.CharField(max_length=255, blank=True, null=True)
    folia = models.CharField(max_length=255, blank=True, null=True)
    lines_per_page = models.CharField(max_length=255, blank=True, null=True)

class TextDecoration(models.Model):
    id = models.AutoField(primary_key=True)
    text_script = models.CharField(max_length=255, blank=True, null=True)
    label_script = models.CharField(max_length=255, blank=True, null=True)
    diagrams = models.BooleanField(blank=True, null=True)
    maps = models.BooleanField(blank=True, null=True)
    illumination = models.BooleanField(blank=True, null=True)
    other = models.CharField(max_length=255, blank=True, null=True)
    relative_quality = models.CharField(max_length=255, blank=True, null=True)

class Detail(models.Model):
    id = models.AutoField(primary_key=True)
    author_attribution = models.CharField(max_length=255, blank=True, null=True)
    scribe_attribution = models.CharField(max_length=255, blank=True, null=True)
    book_headings = models.BooleanField(blank=True, null=True)
    book_headigs_notes = models.CharField(max_length=255, blank=True, null=True)
    book_initials = models.BooleanField(blank=True, null=True)
    book_initials_notes = models.CharField(max_length=255, blank=True, null=True)
    sanza_headings = models.BooleanField(blank=True, null=True)
    sanza_headings_notes = models.CharField(max_length=255, blank=True, null=True)
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
    viewer = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)


class Stanza(models.Model):

    STANZA_LANGUAGE = (
        ('en', 'English'),
        ('it', 'Italian'),
        ('la', 'Latin'),
        ('fr', 'French'),
    )

    id = models.AutoField(primary_key=True)
    stanza_number = models.IntegerField(blank=True, null=True, help_text="The line number of the stanza in the manuscript.")
    stanza_text = models.TextField(blank=True, null=True)
    stanza_notes = models.TextField(blank=True, null=True)
    stanza_translation = models.TextField(blank=True, null=True)
    stanza_language = models.CharField(max_length=2, choices=STANZA_LANGUAGE, blank=True, null=True)
    stanza_translation_notes = models.TextField(blank=True, null=True)
    manuscript = models.ForeignKey('SingleManuscript', on_delete=models.PROTECT, blank=True, null=True)


class SingleManuscript(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    library = models.ForeignKey(ManuscriptLocation, on_delete=models.CASCADE, blank=True, null=True)
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE, blank=True, null=True)
    codex = models.ForeignKey(Codex, on_delete=models.CASCADE, blank=True, null=True)
    text_decorations = models.ForeignKey(TextDecoration, on_delete=models.CASCADE, blank=True, null=True)
    manuscript_details = models.ForeignKey(Detail, on_delete=models.CASCADE, blank=True, null=True)
    viewer_notes = models.ForeignKey(ViewerNote, on_delete=models.CASCADE, blank=True, null=True)