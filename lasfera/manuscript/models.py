from django.db import models


class ManuscriptLocation(models.Model):
    id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    shelfmark = models.CharField(max_length=255, blank=True, null=True)

class EditorialStatus(models.Model):
    id = models.AutoField(primary_key=True)
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

class Manuscript(models.Model):
    id = models.AutoField(primary_key=True)
    text_script = models.CharField(max_length=255, blank=True, null=True)
    label_script = models.CharField(max_length=255, blank=True, null=True)
    diagrams = models.BooleanField(blank=True, null=True)
    maps = models.BooleanField(blank=True, null=True)
    illumination = models.BooleanField(blank=True, null=True)
    other = models.CharField(max_length=255, blank=True, null=True)
    relative_quality = models.CharField(max_length=255, blank=True, null=True)

class Details(models.Model):
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
    distance_numbers = models.BooleanField(blank=True, null=True)
    distance_numbers_notes = models.CharField(max_length=255, blank=True, null=True)
    coat_of_arms = models.BooleanField(blank=True, null=True)
    coat_of_arms_notes = models.CharField(max_length=255, blank=True, null=True)

class ViewerNotes(models.Model):
    id = models.AutoField(primary_key=True)
    date_seen = models.DateField(blank=True, null=True)
    viewer = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

class Stanzas(models.Model):

    STANZA_LANGUAGE = (
        ('en', 'English'),
        ('it', 'Italian'),
        ('la', 'Latin'),
        ('fr', 'French'),
    )

    id = models.AutoField(primary_key=True)
    stanza_number = models.IntegerField(blank=True, null=True)
    stanza_text = models.TextField(blank=True, null=True)
    stanza_notes = models.TextField(blank=True, null=True)
    stanza_translation = models.TextField(blank=True, null=True)
    stanza_language = models.CharField(max_length=2, choices=STANZA_LANGUAGE, blank=True, null=True)
    stanza_translation_notes = models.TextField(blank=True, null=True)